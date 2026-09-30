import AVFoundation
import Network
import Speech

/// Whether the phone has a connection right now, so recognition can fall back
/// from Apple's servers to on-phone when there is none.
final class NetworkStatus: @unchecked Sendable {
    static let shared = NetworkStatus()
    private let monitor = NWPathMonitor()
    private let lock = NSLock()
    private var _online = true

    var online: Bool {
        lock.lock(); defer { lock.unlock() }
        return _online
    }

    private init() {
        monitor.pathUpdateHandler = { [weak self] path in
            guard let self else { return }
            self.lock.lock()
            self._online = path.status == .satisfied
            self.lock.unlock()
        }
        monitor.start(queue: DispatchQueue(label: "vorbeste.network"))
    }
}

/// The microphone tap runs on the audio thread, so the request it feeds lives in
/// a lock-protected box rather than on the main-actor Listener.
private final class RequestBox: @unchecked Sendable {
    private let lock = NSLock()
    private var request: SFSpeechAudioBufferRecognitionRequest?

    func set(_ r: SFSpeechAudioBufferRecognitionRequest?) {
        lock.lock(); request = r; lock.unlock()
    }

    func append(_ buffer: AVAudioPCMBuffer) {
        lock.lock(); let r = request; lock.unlock()
        r?.append(buffer)
    }
}

/// Keeps the microphone open for the whole session and transcribes one answer
/// at a time. Starting and stopping the input per drill would make Bluetooth
/// headphones flip between music and call mode on every question; a steady
/// input also keeps the app alive with the screen locked.
@MainActor
final class Listener {
    private let engine = AVAudioEngine()
    private let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ro-RO"))
    private let box = RequestBox()
    private var task: SFSpeechRecognitionTask?
    private var ticker: Task<Void, Never>?
    private var generation = 0
    private var latest: String?
    private var lastChange = Date()
    private var startedAt = Date()
    private var maxSeconds = 5.0
    private var complete: ((String) -> Bool)?
    private var latestComplete = false
    private var completion: (([String]) -> Void)?
    private var onPartial: ((String) -> Void)?
    private var guesses: [String] = []      // the recogniser's ranked alternatives
    private(set) var running = false

    var isAvailable: Bool { recognizer?.isAvailable ?? false }
    var onDevice: Bool { recognizer?.supportsOnDeviceRecognition ?? false }
    private var lastMode = ""

    /// The "Better recognition" setting: Apple's servers recognise learner
    /// Romanian better than the on-phone model. On by default.
    static var preferServer: Bool {
        UserDefaults.standard.object(forKey: "serverRecognition") as? Bool ?? true
    }

    static func requestPermissions() async -> Bool {
        let status = await withCheckedContinuation {
            (c: CheckedContinuation<SFSpeechRecognizerAuthorizationStatus, Never>) in
            SFSpeechRecognizer.requestAuthorization { c.resume(returning: $0) }
        }
        guard status == .authorized else { return false }
        return await AVAudioApplication.requestRecordPermission()
    }

    func start() throws {
        guard !running else { return }
        let input = engine.inputNode
        let format = input.outputFormat(forBus: 0)
        input.installTap(onBus: 0, bufferSize: 1024, format: format, block: Self.tap(into: box))
        engine.prepare()
        try engine.start()
        running = true
        Log.write("mic on: \(Int(format.sampleRate)) Hz, \(format.channelCount) ch; ro-RO available \(isAvailable), on-device \(onDevice)", "speech")
    }

    /// After an interruption or a route change (AirPods switching between call
    /// and music mode) iOS stops the engine, and the mic's format can change.
    /// Reinstall the tap with the current format and start again.
    func ensureRunning() {
        guard running, !engine.isRunning else { return }
        let input = engine.inputNode
        input.removeTap(onBus: 0)
        let format = input.outputFormat(forBus: 0)
        input.installTap(onBus: 0, bufferSize: 1024, format: format, block: Self.tap(into: box))
        engine.prepare()
        do {
            try engine.start()
            Log.write("mic restarted: \(Int(format.sampleRate)) Hz, \(format.channelCount) ch", "speech")
        } catch {
            Log.write("mic restart failed: \(error)", "speech")
        }
    }

    /// Give up the microphone while paused. With it open, AirPods stay in call
    /// mode and treat a press as a call control, so "play" never arrives.
    /// ensureRunning() takes it back.
    func releaseMic() {
        abort()
        guard running, engine.isRunning else { return }
        engine.stop()
        Log.write("mic released while paused", "speech")
    }

    func stop() {
        abort()
        if running {
            engine.stop()
            engine.inputNode.removeTap(onBus: 0)
            running = false
        }
    }

    /// Listens for one answer and returns the transcript, or nil if nothing was
    /// heard (or the listen was aborted). Ends after speech followed by a short
    /// silence, or at the time limit (extended a little if the learner is
    /// mid-sentence). `onPartial` sees the transcript as it forms.
    /// Returns the recogniser's ranked guesses, best first (up to five), or
    /// none if nothing was heard. `hints` are phrases and words to bias it
    /// toward — the expected answer, its accepted alternatives, its words.
    /// `complete` says whether what has been heard so far is already a whole
    /// answer: then a short silence ends the listen. Otherwise the learner is
    /// probably mid-sentence, recalling the next word, and gets a longer one.
    func listen(expected: String, hints: [String] = [], maxSeconds: Double,
                complete: ((String) -> Bool)? = nil,
                onPartial: ((String) -> Void)? = nil) async -> [String] {
        await withCheckedContinuation { (c: CheckedContinuation<[String], Never>) in
            begin(expected: expected, hints: hints, maxSeconds: maxSeconds, complete: complete,
                  onPartial: onPartial) {
                c.resume(returning: $0)
            }
        }
    }

    /// Ends any listen in progress; its caller gets nil.
    func abort() {
        latest = nil
        guesses = []
        finish()
    }

    private func begin(expected: String, hints: [String], maxSeconds: Double,
                       complete: ((String) -> Bool)?,
                       onPartial: ((String) -> Void)?, completion: @escaping ([String]) -> Void) {
        abort()
        ensureRunning()        // a stopped mic would only ever hear silence
        guard let recognizer, recognizer.isAvailable, running else {
            completion([])
            return
        }
        generation += 1
        let gen = generation
        let req = SFSpeechAudioBufferRecognitionRequest()
        req.shouldReportPartialResults = true
        // Biases recognition toward the words the learner is trying to say,
        // which matters for accented, learner Romanian.
        var context: [String] = []
        for h in [expected] + hints where !h.isEmpty && !context.contains(h) { context.append(h) }
        req.contextualStrings = Array(context.prefix(100))
        // Apple's servers when the setting is on and there is a connection;
        // otherwise on the phone, if this phone can do Romanian on-device.
        let useServer = Self.preferServer && NetworkStatus.shared.online
        req.requiresOnDeviceRecognition = !useServer && recognizer.supportsOnDeviceRecognition
        let mode = req.requiresOnDeviceRecognition ? "on the phone" : "Apple's servers"
        if mode != lastMode {
            Log.write("recognition now via \(mode) (setting: \(Self.preferServer ? "servers" : "phone"), online: \(NetworkStatus.shared.online), on-device possible: \(recognizer.supportsOnDeviceRecognition))", "speech")
            lastMode = mode
        }

        latest = nil
        lastChange = Date()
        startedAt = Date()
        self.maxSeconds = maxSeconds
        self.complete = complete
        latestComplete = false
        self.completion = completion
        self.onPartial = onPartial
        box.set(req)
        task = recognizer.recognitionTask(with: req, resultHandler: Self.handler(for: self, gen: gen))
        ticker = Task { [weak self] in
            while !Task.isCancelled {
                try? await Task.sleep(nanoseconds: 200_000_000)
                self?.tick(gen)
            }
        }
    }

    // Built outside the main actor: these closures are called on audio and
    // recognition threads, and must not inherit main-actor isolation.
    nonisolated private static func tap(into box: RequestBox) -> AVAudioNodeTapBlock {
        { buffer, _ in box.append(buffer) }
    }

    nonisolated private static func handler(for listener: Listener, gen: Int)
        -> (SFSpeechRecognitionResult?, Error?) -> Void {
        { [weak listener] result, error in
            // best first, then the other ranked alternatives, without repeats
            var texts: [String] = []
            if let result {
                for t in [result.bestTranscription] + result.transcriptions {
                    let s = t.formattedString
                    if !s.isEmpty && !texts.contains(s) { texts.append(s) }
                }
            }
            let ranked = Array(texts.prefix(5))
            let isFinal = result?.isFinal ?? false
            let failed = error != nil
            if let error {
                let e = error as NSError
                // 1110 "no speech detected" and 216/301 "cancelled" are routine.
                if ![1110, 216, 301].contains(e.code) {
                    Log.write("recognition error \(e.domain) \(e.code): \(e.localizedDescription)", "speech")
                }
            }
            Task { @MainActor in
                listener?.update(gen: gen, texts: ranked, isFinal: isFinal, failed: failed)
            }
        }
    }

    private func update(gen: Int, texts: [String], isFinal: Bool, failed: Bool) {
        guard gen == generation, completion != nil else { return }
        if !texts.isEmpty { guesses = texts }
        if let text = texts.first, text != latest {
            latest = text
            latestComplete = complete?(text) ?? true
            lastChange = Date()
            onPartial?(text)
        }
        if isFinal || failed { finish() }
    }

    private func tick(_ gen: Int) {
        guard gen == generation, completion != nil else { return }
        let now = Date()
        // Learners pause mid-answer to recall the next word, and the 1.3 s
        // that ended every listen cut them off ("Fiul meu e" for "Fiul meu e
        // elev", then right on the retry). A whole answer still ends fast.
        let limit = latest == nil ? maxSeconds : maxSeconds + 8
        let quiet = latestComplete ? 1.0 : 2.8
        let spokeThenStopped = latest != nil && now.timeIntervalSince(lastChange) > quiet
        if spokeThenStopped || now.timeIntervalSince(startedAt) > limit { finish() }
    }

    private func finish() {
        let done = completion
        completion = nil
        onPartial = nil
        complete = nil
        let heard = latest == nil ? [] : (guesses.isEmpty ? [latest!] : guesses)
        guesses = []
        cancelCurrent()
        done?(heard)
    }

    private func cancelCurrent() {
        ticker?.cancel()
        ticker = nil
        box.set(nil)
        task?.cancel()
        task = nil
    }
}
