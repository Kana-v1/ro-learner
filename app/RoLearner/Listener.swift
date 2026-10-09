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

/// What the microphone picked up during one listen, from its loudness alone:
/// whether a voice was there at all, independent of what the recogniser made
/// of it. Separates "the learner said nothing" from "the recogniser missed it".
struct VoiceMeter: Sendable {
    var firstVoice: Double?       // CFAbsoluteTime of the first voiced buffer
    var lastVoice: Double?        // ... and the latest
    var voicedSeconds = 0.0
    var peakDB = -160.0
    var floorDB = -60.0           // running estimate of the background noise
}

/// The microphone tap runs on the audio thread, so the request it feeds — and
/// the loudness meter — live in a lock-protected box rather than on the
/// main-actor Listener.
private final class RequestBox: @unchecked Sendable {
    private let lock = NSLock()
    private var request: SFSpeechAudioBufferRecognitionRequest?
    private var meter = VoiceMeter()
    private var floor: Double?
    // The answer as Whisper wants it: 16 kHz mono floats. Converted on the
    // audio thread as it arrives; the converter is only touched there.
    private var capturing = false
    private var samples: [Float] = []
    private var converter: AVAudioConverter?
    private var converterInput: AVAudioFormat?
    private let whisperFormat = AVAudioFormat(commonFormat: .pcmFormatFloat32, sampleRate: 16_000,
                                              channels: 1, interleaved: false)!

    func startCapture() {
        lock.lock(); samples = []; capturing = true; lock.unlock()
    }

    /// Stop recording and hand over what was recorded.
    func stopCapture() -> [Float] {
        lock.lock(); defer { lock.unlock() }
        capturing = false
        let out = samples
        samples = []
        return out
    }

    func set(_ r: SFSpeechAudioBufferRecognitionRequest?) {
        lock.lock(); request = r; lock.unlock()
    }

    /// Start a fresh meter for a new listen; the noise floor carries over.
    func resetMeter() {
        lock.lock(); meter = VoiceMeter(floorDB: floor ?? -60); lock.unlock()
    }

    func reading() -> VoiceMeter {
        lock.lock(); defer { lock.unlock() }
        return meter
    }

    func append(_ buffer: AVAudioPCMBuffer) {
        let db = Self.level(buffer)
        lock.lock()
        let r = request
        if let db, buffer.format.sampleRate > 0 {
            // The floor drops quickly to quiet moments and rises slowly, so a
            // steady background (traffic, wind) becomes the floor and a voice
            // stands out above it.
            let f = floor ?? db
            floor = db < f ? f * 0.7 + db * 0.3 : f * 0.995 + db * 0.005
            meter.floorDB = floor!
            meter.peakDB = max(meter.peakDB, db)
            if db > meter.floorDB + 12 && db > -55 {
                let now = CFAbsoluteTimeGetCurrent()
                if meter.firstVoice == nil { meter.firstVoice = now }
                meter.lastVoice = now
                meter.voicedSeconds += Double(buffer.frameLength) / buffer.format.sampleRate
            }
        }
        let capture = capturing
        lock.unlock()
        r?.append(buffer)
        if capture, let converted = resample(buffer) {
            lock.lock()
            if capturing { samples.append(contentsOf: converted) }
            lock.unlock()
        }
    }

    private func resample(_ buffer: AVAudioPCMBuffer) -> [Float]? {
        if converter == nil || converterInput != buffer.format {
            converter = AVAudioConverter(from: buffer.format, to: whisperFormat)
            converterInput = buffer.format
        }
        guard let converter, buffer.format.sampleRate > 0 else { return nil }
        let capacity = AVAudioFrameCount(Double(buffer.frameLength) * 16_000 / buffer.format.sampleRate) + 64
        guard let out = AVAudioPCMBuffer(pcmFormat: whisperFormat, frameCapacity: capacity) else { return nil }
        var fed = false
        var error: NSError?
        converter.convert(to: out, error: &error) { _, status in
            if fed {
                status.pointee = .noDataNow
                return nil
            }
            fed = true
            status.pointee = .haveData
            return buffer
        }
        guard error == nil, let data = out.floatChannelData?[0] else { return nil }
        return Array(UnsafeBufferPointer(start: data, count: Int(out.frameLength)))
    }

    /// Loudness of one buffer in dB (RMS of the first channel).
    private static func level(_ buffer: AVAudioPCMBuffer) -> Double? {
        guard let data = buffer.floatChannelData?[0], buffer.frameLength > 0 else { return nil }
        let n = Int(buffer.frameLength)
        var sum: Float = 0
        for i in 0..<n { sum += data[i] * data[i] }
        let rms = (sum / Float(n)).squareRoot()
        return 20 * log10(Double(max(rms, 1e-8)))
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
    private var request: SFSpeechAudioBufferRecognitionRequest?
    private var task: SFSpeechRecognitionTask?
    private var ticker: Task<Void, Never>?
    private var generation = 0
    private var latest: String?
    private var lastChange = 0.0              // CFAbsoluteTime, like the meter's
    private var startedAt = 0.0
    private var maxSeconds = 5.0
    private var finalizing = false            // input ended, waiting for the final result(s)
    private var finalDeadline = 0.0
    private var gotFinal = false
    private var appleDone = false
    // Whisper, when it is the chosen recogniser: it transcribes the recorded
    // answer once the learner has finished, alongside Apple's final result.
    private var useWhisper = false
    private var whisperPrompt = ""
    private var whisperDone = true
    private var whisperDeadline = 0.0
    private var whisperText: String?
    private var whisperTask: Task<Void, Never>?
    private var complete: ((String) -> Bool)?
    private var latestComplete = false
    private var completion: (([String]) -> Void)?
    private var onPartial: ((String) -> Void)?
    private var guesses: [String] = []      // the recogniser's ranked alternatives
    private(set) var running = false
    /// How the last listen went, for the log and the results: was a voice
    /// there, and did the recogniser deliver its final result.
    private(set) var lastMeter = VoiceMeter()
    private(set) var lastWasFinal = false
    private(set) var lastMode = ""
    /// Whisper's transcript of the last answer (nil when Whisper wasn't used
    /// or heard nothing), whether it was used, and how long it took.
    private(set) var lastWhisper: String?
    private(set) var lastUsedWhisper = false
    private(set) var lastWhisperSeconds = 0.0

    var isAvailable: Bool { recognizer?.isAvailable ?? false }
    var onDevice: Bool { recognizer?.supportsOnDeviceRecognition ?? false }

    /// Settings → Recognition. "whisper" (the default): Whisper on the phone
    /// (WhisperEngine), with Apple's recogniser running alongside to tell when
    /// the answer is over; until Whisper is downloaded and ready, Apple's
    /// alone. "server": Apple's servers. "phone": Apple, on the phone.
    /// ("tuned", an earlier setting, was an Apple custom language model that
    /// iOS cannot build for Romanian; it now means Whisper.)
    static var mode: String {
        let m = UserDefaults.standard.string(forKey: "recognitionMode") ?? "whisper"
        return m == "tuned" ? "whisper" : m
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
    func listen(expected: String, hints: [String] = [], prompt: String? = nil, maxSeconds: Double,
                complete: ((String) -> Bool)? = nil,
                onPartial: ((String) -> Void)? = nil) async -> [String] {
        await withCheckedContinuation { (c: CheckedContinuation<[String], Never>) in
            begin(expected: expected, hints: hints, prompt: prompt ?? expected, maxSeconds: maxSeconds,
                  complete: complete, onPartial: onPartial) {
                c.resume(returning: $0)
            }
        }
    }

    /// Ends any listen in progress; its caller gets nil.
    func abort() {
        latest = nil
        guesses = []
        whisperText = nil
        finish()
    }

    private func begin(expected: String, hints: [String], prompt: String, maxSeconds: Double,
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
        // Apple's recogniser: its servers when chosen (or alongside Whisper)
        // and online, else the phone if it can.
        let canPhone = recognizer.supportsOnDeviceRecognition
        let useServer = Self.mode != "phone" && NetworkStatus.shared.online
        req.requiresOnDeviceRecognition = !useServer && canPhone
        useWhisper = Self.mode == "whisper" && WhisperEngine.shared.isReady
        let apple = req.requiresOnDeviceRecognition ? "Apple on the phone" : "Apple's servers"
        let mode = useWhisper ? "Whisper on the phone (\(apple) alongside)" : apple
        if mode != lastMode {
            Log.write("recognition now via \(mode) (setting: \(Self.mode), online: \(NetworkStatus.shared.online), whisper: \(WhisperEngine.shared.statusText))", "speech")
            lastMode = mode
        }
        whisperPrompt = prompt
        whisperText = nil
        whisperDone = true
        appleDone = false
        if useWhisper { box.startCapture() }

        latest = nil
        lastChange = CFAbsoluteTimeGetCurrent()
        startedAt = lastChange
        finalizing = false
        gotFinal = false
        box.resetMeter()
        request = req
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
            lastChange = CFAbsoluteTimeGetCurrent()
            onPartial?(text)
        }
        if isFinal { gotFinal = true }
        if isFinal || failed {
            // The recogniser can end on its own; Whisper still gets the audio.
            if !finalizing { endInput() }
            appleDone = true
            tryFinish()
        }
    }

    /// When to stop listening. Silence is measured from the later of the last
    /// change in the transcript and the last moment the mic heard a voice, so
    /// a word still being said (or not yet transcribed) keeps the listen open.
    private func tick(_ gen: Int) {
        guard gen == generation, completion != nil else { return }
        let now = CFAbsoluteTimeGetCurrent()
        if finalizing {
            if !appleDone && now > finalDeadline {
                Log.write("no final result in time; using the last partial", "speech")
                appleDone = true
            }
            if !whisperDone && now > whisperDeadline {
                Log.write("whisper took too long; using Apple's result", "speech")
                whisperDone = true
            }
            tryFinish()
            return
        }
        let meter = box.reading()
        let spoke = latest != nil || meter.lastVoice != nil
        let lastActivity = max(latest != nil ? lastChange : 0, meter.lastVoice ?? 0)
        // Learners pause mid-answer to recall the next word; a whole answer
        // still ends fast.
        let quiet = latestComplete ? 0.9 : 2.4
        if spoke && now - lastActivity > quiet {
            endInput()
        } else if !spoke && now - startedAt > maxSeconds {
            finish()
        } else if now - startedAt > maxSeconds + 8 {
            endInput()
        }
    }

    /// The learner has finished: stop feeding audio and ask for the final
    /// result. Partial results trail the audio, and for a short word there may
    /// be none at all before the end — cancelling here, as this used to, threw
    /// away exactly the last word or the only word ("La" for "larg", nothing
    /// for "mic"). The final result is where the recogniser commits them.
    private func endInput() {
        guard !finalizing else { return }
        finalizing = true
        box.set(nil)
        request?.endAudio()
        let now = CFAbsoluteTimeGetCurrent()
        finalDeadline = now + 2.0
        guard useWhisper else { return }
        let audio = box.stopCapture()
        // Only when the mic heard a voice: Whisper invents text for silence.
        guard box.reading().voicedSeconds >= 0.15, audio.count >= 1_600 else { return }
        whisperDone = false
        whisperDeadline = now + 8.0
        let gen = generation
        let prompt = whisperPrompt
        whisperTask = Task { [weak self] in
            let started = CFAbsoluteTimeGetCurrent()
            let text = await WhisperEngine.shared.transcribe(audio, prompt: prompt)
            guard let self, gen == self.generation, self.completion != nil else { return }
            self.whisperText = text
            self.lastWhisperSeconds = CFAbsoluteTimeGetCurrent() - started
            self.whisperDone = true
            self.tryFinish()
        }
    }

    private func tryFinish() {
        if finalizing && appleDone && whisperDone { finish() }
    }

    private func finish() {
        let done = completion
        completion = nil
        onPartial = nil
        complete = nil
        let heard = latest == nil ? [] : (guesses.isEmpty ? [latest!] : guesses)
        guesses = []
        lastMeter = box.reading()
        lastWasFinal = gotFinal
        lastWhisper = whisperText
        lastUsedWhisper = useWhisper
        cancelCurrent()
        done?(heard)
    }

    private func cancelCurrent() {
        ticker?.cancel()
        ticker = nil
        box.set(nil)
        task?.cancel()
        task = nil
        request = nil
        finalizing = false
        _ = box.stopCapture()
        whisperTask?.cancel()
        whisperTask = nil
        whisperDone = true
        appleDone = false
    }
}
