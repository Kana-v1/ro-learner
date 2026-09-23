import AVFoundation
import MediaPlayer
import SwiftUI

/// Runs one listen-through of an episode.
///
/// Voice mode: play until a cue has been spoken, pause, listen for the answer,
/// grade it, play a short tone, then play the episode's own correct answer and
/// carry on. At the end, drills that were missed or only close are asked again
/// (the "second chance" round), replaying the cue from the episode audio.
///
/// Tap mode (no microphone or no Romanian recognition): the episode plays
/// straight through with its designed pauses; the learner marks misses with the
/// on-screen button or the headphones' previous-track press.
@MainActor
final class SessionEngine: ObservableObject {
    enum Phase { case idle, playing, listening, feedback, paused, finished }

    @Published private(set) var phase: Phase = .idle
    @Published private(set) var lastCue: String?
    @Published private(set) var lastExpected: String?
    @Published private(set) var lastHeard: String?
    @Published private(set) var lastVerdict: Verdict?
    @Published private(set) var done = 0
    @Published private(set) var correctCount = 0
    @Published private(set) var inRetry = false
    @Published private(set) var note: String?
    @Published private(set) var voiceMode: Bool

    let pack: Pack
    let drills: [Drill]
    var total: Int { drills.count }

    private let store: PackStore
    private let headsetMic: Bool
    private let listener = Listener()
    private let tones = Tones()
    private let speech = AVSpeechSynthesizer()
    private let player: AVPlayer
    private var timeObserver: Any?
    private var endObserver: NSObjectProtocol?
    private var record: SessionRecord

    private var next = 0                  // main pass: the next cue to stop at
    private var retryQueue: [Drill] = []
    private var awaitingCue: Drill?       // retry: stop once this cue is spoken
    private var stopAt: Double?           // retry: stop once the answer has played
    private var busy = false              // listening or giving feedback

    init(pack: Pack, store: PackStore, voiceMode: Bool, headsetMic: Bool) {
        self.pack = pack
        self.store = store
        self.voiceMode = voiceMode
        self.headsetMic = headsetMic
        drills = pack.header.drills
        player = AVPlayer(url: pack.audioURL)
        record = SessionRecord(episode: pack.header.slug, title: pack.header.title,
                               started: Date(), finished: nil,
                               mode: voiceMode ? "voice" : "tap", items: [])
    }

    // MARK: lifecycle

    func start() async {
        guard phase == .idle else { return }
        if voiceMode {
            if await Listener.requestPermissions() == false {
                voiceMode = false
                note = "Microphone or speech recognition permission is off, so this is tap mode."
            } else if !listener.isAvailable {
                voiceMode = false
                note = "Romanian speech recognition isn't available right now, so this is tap mode."
            }
        }
        configureAudio()
        if voiceMode && !listener.onDevice {
            note = "Romanian recognition runs on Apple's servers here, so it needs mobile data."
        }
        record.mode = voiceMode ? "voice" : "tap"

        timeObserver = player.addPeriodicTimeObserver(
            forInterval: CMTime(value: 1, timescale: 20), queue: .main
        ) { [weak self] time in
            MainActor.assumeIsolated { self?.tick(time.seconds) }
        }
        endObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime, object: player.currentItem, queue: .main
        ) { [weak self] _ in
            MainActor.assumeIsolated { self?.reachedEnd() }
        }
        setupRemoteCommands()
        phase = .playing
        player.play()
        updateNowPlaying()
    }

    private func configureAudio() {
        let session = AVAudioSession.sharedInstance()
        do {
            if voiceMode {
                var options: AVAudioSession.CategoryOptions = [.allowBluetoothA2DP, .defaultToSpeaker]
                // The headphone mic hears you far better while walking, at the
                // cost of call-quality playback on Bluetooth headphones.
                if headsetMic { options.insert(.allowBluetooth) }
                try session.setCategory(.playAndRecord, mode: .default, options: options)
                try session.setActive(true)
                try listener.start()
            } else {
                try session.setCategory(.playback, mode: .spokenAudio)
                try session.setActive(true)
            }
        } catch {
            voiceMode = false
            note = "Couldn't start the microphone (\(error.localizedDescription)), so this is tap mode."
            try? session.setCategory(.playback, mode: .spokenAudio)
            try? session.setActive(true)
        }
    }

    func stop() {
        player.pause()
        if let o = timeObserver { player.removeTimeObserver(o); timeObserver = nil }
        if let o = endObserver { NotificationCenter.default.removeObserver(o); endObserver = nil }
        listener.stop()
        speech.stopSpeaking(at: .immediate)
        let c = MPRemoteCommandCenter.shared()
        for cmd in [c.playCommand, c.pauseCommand, c.togglePlayPauseCommand,
                    c.nextTrackCommand, c.previousTrackCommand] {
            cmd.removeTarget(nil)
        }
        MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
        if !record.items.isEmpty { store.save(record) }
        store.reload()
        try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
    }

    func togglePause() {
        switch phase {
        case .playing: player.pause(); phase = .paused
        case .paused: player.play(); phase = .playing
        default: break
        }
        updateNowPlaying()
    }

    /// Correct the automatic verdict on the most recent drill — the recogniser
    /// will sometimes mishear a right answer, or accept a wrong one.
    func override(_ v: Verdict) {
        guard let i = record.items.indices.last else { return }
        let old = record.items[i].verdict
        guard old != v else { return }
        record.items[i].verdict = v
        record.items[i].overridden = true
        if !record.items[i].retry {
            if old == .correct { correctCount -= 1 }
            if v == .correct { correctCount += 1 }
        }
        lastVerdict = v
        tones.play(v)
        store.save(record)
    }

    // MARK: the drill loop

    private func tick(_ t: Double) {
        guard phase == .playing, !busy else { return }
        if inRetry {
            if let d = awaitingCue, t >= d.promptEnd - 0.03 {
                awaitingCue = nil
                cue(d)
            } else if let s = stopAt, t >= s {
                stopAt = nil
                player.pause()
                nextRetry()
            }
            return
        }
        guard next < drills.count else { return }
        let d = drills[next]
        if t >= d.promptEnd - 0.03 {
            next += 1
            cue(d)
        }
    }

    private func cue(_ d: Drill) {
        lastCue = d.cue
        lastExpected = d.expected
        guard voiceMode else {
            append(d, heard: nil, score: 0, verdict: .unmarked)
            lastHeard = nil
            lastVerdict = nil
            if inRetry { stopAt = d.answerEnd + 0.4 }
            return
        }
        busy = true
        player.pause()
        phase = .listening
        lastHeard = nil
        lastVerdict = nil
        updateNowPlaying()
        listener.listen(expected: d.expected, maxSeconds: max(d.thinkSeconds + 1.5, 4)) { [weak self] heard in
            self?.grade(d, heard: heard)
        }
    }

    private func grade(_ d: Drill, heard: String?) {
        let score = heard.map { Grader.score(expected: d.expected, heard: $0) } ?? 0
        let verdict = Grader.verdict(score: score, heard: heard)
        append(d, heard: heard, score: score, verdict: verdict)
        lastHeard = heard
        lastVerdict = verdict
        phase = .feedback
        tones.play(verdict)
        Task { @MainActor [weak self] in
            try? await Task.sleep(nanoseconds: 450_000_000)
            await self?.playAnswer(d)
        }
    }

    private func playAnswer(_ d: Drill) async {
        guard phase == .feedback else { return }
        _ = await player.seek(to: CMTime(seconds: d.answerStart, preferredTimescale: 600),
                              toleranceBefore: .zero, toleranceAfter: .zero)
        if inRetry { stopAt = d.answerEnd + 0.4 }
        busy = false
        phase = .playing
        player.play()
        updateNowPlaying()
    }

    private func append(_ d: Drill, heard: String?, score: Double, verdict: Verdict) {
        record.items.append(DrillResult(seg: d.id, cue: d.cue, expected: d.expected,
                                        heard: heard, score: score, verdict: verdict,
                                        overridden: false, retry: inRetry, chapter: d.chapter))
        if !inRetry {
            done += 1
            if verdict == .correct { correctCount += 1 }
        }
        store.save(record)
    }

    // MARK: second chance

    private func reachedEnd() {
        if inRetry {
            if !busy && phase == .playing {
                stopAt = nil
                nextRetry()
            }
            return
        }
        beginRetry()
    }

    private func beginRetry() {
        var latest: [Int: Verdict] = [:]
        for it in record.items where !it.retry { latest[it.seg] = it.verdict }
        retryQueue = drills.filter { d in
            guard let v = latest[d.id] else { return false }
            return v == .missed || v == .noAnswer || v == .close
        }
        guard !retryQueue.isEmpty else { finish(); return }
        inRetry = true
        player.pause()
        say("Second chance. \(retryQueue.count) to try again.")
        Task { @MainActor [weak self] in
            try? await Task.sleep(nanoseconds: 3_000_000_000)
            self?.nextRetry()
        }
    }

    private func nextRetry() {
        guard !retryQueue.isEmpty else { finish(); return }
        let d = retryQueue.removeFirst()
        awaitingCue = d
        Task { @MainActor [weak self] in
            guard let self else { return }
            _ = await self.player.seek(to: CMTime(seconds: d.promptStart, preferredTimescale: 600),
                                       toleranceBefore: .zero, toleranceAfter: .zero)
            self.phase = .playing
            self.player.play()
            self.updateNowPlaying()
        }
    }

    private func finish() {
        guard phase != .finished else { return }
        player.pause()
        phase = .finished
        record.finished = Date()
        store.save(record)
        listener.stop()
        if voiceMode {
            say("Done. \(correctCount) of \(total) right first time.")
        }
        updateNowPlaying()
    }

    // MARK: system integration

    /// English only: the course never has an English voice speak Romanian.
    private func say(_ text: String) {
        let u = AVSpeechUtterance(string: text)
        u.voice = AVSpeechSynthesisVoice(language: "en-US")
        speech.speak(u)
    }

    /// Headphone and lock-screen buttons: play/pause as usual; "next track"
    /// says the last answer was right, "previous track" says it was wrong.
    private func setupRemoteCommands() {
        let c = MPRemoteCommandCenter.shared()
        c.togglePlayPauseCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.togglePause() }
            return .success
        }
        c.playCommand.addTarget { [weak self] _ in
            Task { @MainActor in if self?.phase == .paused { self?.togglePause() } }
            return .success
        }
        c.pauseCommand.addTarget { [weak self] _ in
            Task { @MainActor in if self?.phase == .playing { self?.togglePause() } }
            return .success
        }
        c.nextTrackCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.override(.correct) }
            return .success
        }
        c.previousTrackCommand.addTarget { [weak self] _ in
            Task { @MainActor in self?.override(.missed) }
            return .success
        }
    }

    private func updateNowPlaying() {
        let info: [String: Any] = [
            MPMediaItemPropertyTitle: pack.header.title,
            MPMediaItemPropertyArtist: inRetry ? "Second chance" : "Romanian · \(done)/\(total)",
            MPMediaItemPropertyPlaybackDuration: pack.header.duration,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: player.currentTime().seconds,
            MPNowPlayingInfoPropertyPlaybackRate: phase == .playing ? 1.0 : 0.0,
        ]
        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }
}

/// Short feedback tones, synthesised once at start-up so nothing needs bundling.
final class Tones {
    private var players: [Verdict: AVAudioPlayer] = [:]

    init() {
        players[.correct] = Self.make([880, 1320])
        players[.close] = Self.make([660, 660])
        players[.missed] = Self.make([330, 247])
        players[.noAnswer] = Self.make([247])
    }

    func play(_ v: Verdict) {
        guard let p = players[v] else { return }
        p.currentTime = 0
        p.play()
    }

    private static func make(_ freqs: [Double]) -> AVAudioPlayer? {
        let rate = 44100.0
        let noteLength = 0.12
        var samples: [Int16] = []
        for f in freqs {
            let n = Int(rate * noteLength)
            for i in 0..<n {
                let envelope = min(1.0, Double(i) / 400.0, Double(n - i) / 400.0)
                samples.append(Int16(sin(2 * .pi * f * Double(i) / rate) * envelope * 12000))
            }
        }
        var d = Data()
        func u32(_ v: UInt32) { withUnsafeBytes(of: v.littleEndian) { d.append(contentsOf: $0) } }
        func u16(_ v: UInt16) { withUnsafeBytes(of: v.littleEndian) { d.append(contentsOf: $0) } }
        let dataBytes = UInt32(samples.count * 2)
        d.append(contentsOf: Array("RIFF".utf8)); u32(36 + dataBytes)
        d.append(contentsOf: Array("WAVE".utf8))
        d.append(contentsOf: Array("fmt ".utf8)); u32(16); u16(1); u16(1); u32(44100); u32(88200); u16(2); u16(16)
        d.append(contentsOf: Array("data".utf8)); u32(dataBytes)
        samples.withUnsafeBytes { d.append(contentsOf: $0) }
        return try? AVAudioPlayer(data: d)
    }
}
