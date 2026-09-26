import AVFoundation
import Speech

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
    private var completion: ((String?) -> Void)?
    private var onPartial: ((String) -> Void)?
    private(set) var running = false

    var isAvailable: Bool { recognizer?.isAvailable ?? false }
    var onDevice: Bool { recognizer?.supportsOnDeviceRecognition ?? false }

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
    func listen(expected: String, maxSeconds: Double,
                onPartial: ((String) -> Void)? = nil) async -> String? {
        await withCheckedContinuation { (c: CheckedContinuation<String?, Never>) in
            begin(expected: expected, maxSeconds: maxSeconds, onPartial: onPartial) {
                c.resume(returning: $0)
            }
        }
    }

    /// Ends any listen in progress; its caller gets nil.
    func abort() {
        latest = nil
        finish()
    }

    private func begin(expected: String, maxSeconds: Double, onPartial: ((String) -> Void)?,
                       completion: @escaping (String?) -> Void) {
        abort()
        ensureRunning()        // a stopped mic would only ever hear silence
        guard let recognizer, recognizer.isAvailable, running else {
            completion(nil)
            return
        }
        generation += 1
        let gen = generation
        let req = SFSpeechAudioBufferRecognitionRequest()
        req.shouldReportPartialResults = true
        // Biases recognition toward the words the learner is trying to say,
        // which matters for accented, learner Romanian.
        req.contextualStrings = [expected]
        if recognizer.supportsOnDeviceRecognition { req.requiresOnDeviceRecognition = true }

        latest = nil
        lastChange = Date()
        startedAt = Date()
        self.maxSeconds = maxSeconds
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
            let text = result?.bestTranscription.formattedString
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
                listener?.update(gen: gen, text: text, isFinal: isFinal, failed: failed)
            }
        }
    }

    private func update(gen: Int, text: String?, isFinal: Bool, failed: Bool) {
        guard gen == generation, completion != nil else { return }
        if let text, !text.isEmpty, text != latest {
            latest = text
            lastChange = Date()
            onPartial?(text)
        }
        if isFinal || failed { finish() }
    }

    private func tick(_ gen: Int) {
        guard gen == generation, completion != nil else { return }
        let now = Date()
        let limit = latest == nil ? maxSeconds : maxSeconds + 3
        let spokeThenStopped = latest != nil && now.timeIntervalSince(lastChange) > 1.3
        if spokeThenStopped || now.timeIntervalSince(startedAt) > limit { finish() }
    }

    private func finish() {
        let done = completion
        completion = nil
        onPartial = nil
        let heard = latest
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
