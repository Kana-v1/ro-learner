import AVFoundation
import MediaPlayer
import SwiftUI

/// Runs one listen-through of an episode.
///
/// Voice mode: play until a cue has been spoken, pause, chime, listen, grade. A
/// miss or a non-answer gets a second try straight away: a spoken "once more",
/// the cue replayed from the episode, a second listen. Then the verdict is
/// spoken and the episode's own answer plays. After the last drill, anything
/// still wrong is asked again (the end-of-episode second chance).
///
/// Everything the learner needs is audible, so it works with the phone in a
/// pocket. Headphone next/previous jump between drills.
///
/// Tap mode (no microphone or no Romanian recognition): the episode plays
/// straight through with its designed pauses; misses are marked by hand.
@MainActor
final class SessionEngine: ObservableObject {
    enum Phase: Equatable { case idle, playing, paused, listening, secondTry, feedback, finished }

    @Published private(set) var phase: Phase = .idle
    @Published private(set) var position: Double = 0
    @Published private(set) var current: Drill?
    @Published private(set) var attempt = 1
    @Published private(set) var liveHeard: String?
    @Published private(set) var lastHeard: String?
    @Published private(set) var lastVerdict: Verdict?
    @Published private(set) var lastHint: String?
    @Published private(set) var inRound = false
    @Published private(set) var roundDone = 0
    @Published private(set) var roundTotal = 0
    @Published private(set) var note: String?
    @Published private(set) var voiceMode: Bool
    @Published private(set) var record: SessionRecord

    let pack: Pack
    let drills: [Drill]
    let chapters: [Chapter]
    var duration: Double { pack.header.duration }
    var total: Int { drills.count }
    var rightFirstTime: Int { record.rightFirstTime }
    var markedWrong: Int { record.mainItems.filter { $0.outcome == .missed }.count }
    var fixedInRound: Int { record.items.filter { $0.round == 1 && $0.outcome == .correct }.count }
    var currentChapter: Chapter? { chapters.last { $0.start <= position + 0.05 } }

    var drillLabel: String {
        if inRound { return "\(min(roundDone + 1, roundTotal))/\(roundTotal)" }
        let k = current.flatMap(index(of:)) ?? max(next - 1, 0)
        return "\(min(k + 1, total))/\(total)"
    }

    /// The most recent result for each drill that is still not right.
    var stillToWorkOn: [DrillResult] {
        var latest: [Int: DrillResult] = [:]
        for it in record.items where it.outcome != .unmarked { latest[it.seg] = it }
        return drills.compactMap { latest[$0.id] }.filter { $0.outcome != .correct }
    }

    private let store: PackStore
    private let headsetMic: Bool
    private let listener = Listener()
    private let tones = Tones()
    private let coach = Coach()
    private let player: AVPlayer
    private let startAt: Double
    private var timeObserver: Any?
    private var observers: [NSObjectProtocol] = []
    private var next = 0                       // main pass: the next cue to stop at
    private var flow: Task<Void, Never>?       // the drill (or second-chance round) in progress
    private var waiter: (time: Double, cont: CheckedContinuation<Bool, Never>)?
    private var roundQueue: [Drill] = []
    private var resumeDrill: Drill?            // paused mid-drill: its cue replays on resume
    private var lastPersist = Date()
    // While a seek is on its way the player still reports the old position;
    // acting on it would start a drill the learner just jumped away from.
    private var seeking = false
    private var relocateGen = 0
    private var pausedByInterruption = false
    private var closed = false

    init(pack: Pack, store: PackStore, voiceMode: Bool, headsetMic: Bool, resume: SavedProgress?) {
        self.pack = pack
        self.store = store
        self.voiceMode = voiceMode
        self.headsetMic = headsetMic
        drills = pack.header.drills
        chapters = pack.header.chapters
        player = AVPlayer(url: pack.audioURL)
        record = resume?.record ?? SessionRecord(episode: pack.header.slug, title: pack.header.title,
                                                 started: Date(), finished: nil,
                                                 mode: voiceMode ? "voice" : "tap", items: [])
        startAt = resume?.position ?? 0
        position = startAt
    }

    // MARK: lifecycle

    func start() async {
        guard phase == .idle else { return }
        if voiceMode {
            if await Listener.requestPermissions() == false {
                voiceMode = false
                note = "Microphone or speech recognition is off, so this is tap mode."
            } else if !listener.isAvailable {
                voiceMode = false
                note = "Romanian speech recognition isn't available right now, so this is tap mode."
            }
        }
        configureAudio()
        if voiceMode && !listener.onDevice {
            note = "Romanian recognition runs on Apple's servers on this phone, so it needs mobile data."
        }
        record.mode = voiceMode ? "voice" : "tap"
        Log.write("start \(pack.header.slug) in \(record.mode) mode at \(timeString(startAt)); \(total) drills; on-device recognition: \(listener.onDevice)", "player")

        timeObserver = player.addPeriodicTimeObserver(
            forInterval: CMTime(value: 1, timescale: 10), queue: .main
        ) { [weak self] time in
            MainActor.assumeIsolated { self?.tick(time.seconds) }
        }
        let nc = NotificationCenter.default
        observers.append(nc.addObserver(forName: .AVPlayerItemDidPlayToEndTime,
                                        object: player.currentItem, queue: .main) { [weak self] _ in
            MainActor.assumeIsolated { self?.reachedEnd() }
        })
        // A phone call, or headphones unplugged: pause like any audio app.
        observers.append(nc.addObserver(forName: AVAudioSession.interruptionNotification,
                                        object: nil, queue: .main) { [weak self] n in
            let type = n.userInfo?[AVAudioSessionInterruptionTypeKey] as? UInt
            let began = type == AVAudioSession.InterruptionType.began.rawValue
            let options = n.userInfo?[AVAudioSessionInterruptionOptionKey] as? UInt ?? 0
            let shouldResume = AVAudioSession.InterruptionOptions(rawValue: options).contains(.shouldResume)
            MainActor.assumeIsolated { self?.interrupted(began: began, shouldResume: shouldResume) }
        })
        observers.append(nc.addObserver(forName: AVAudioSession.routeChangeNotification,
                                        object: nil, queue: .main) { [weak self] n in
            let reason = n.userInfo?[AVAudioSessionRouteChangeReasonKey] as? UInt
            let lost = reason == AVAudioSession.RouteChangeReason.oldDeviceUnavailable.rawValue
            let route = AVAudioSession.sharedInstance().currentRoute
            let desc = "out \(route.outputs.map(\.portName)) in \(route.inputs.map(\.portName))"
            Log.write("route change (reason \(reason ?? 0)): \(desc)", "audio")
            MainActor.assumeIsolated { if lost { self?.pauseIfRunning() } }
        })
        setupRemoteCommands()

        next = firstDrill(endingAfter: startAt)
        if startAt > 0 { await seekTo(startAt) }
        if startAt >= duration - 0.5 {
            phase = .playing
            beginRound()
            return
        }
        phase = .playing
        player.play()
        updateNowPlaying()
    }

    /// Listening needs play-and-record; the headphone mic hears you far better
    /// while walking, at the cost of call-quality playback on Bluetooth.
    private func setListeningCategory() throws {
        var options: AVAudioSession.CategoryOptions = [.allowBluetoothA2DP, .defaultToSpeaker]
        if headsetMic { options.insert(.allowBluetooth) }
        try AVAudioSession.sharedInstance().setCategory(.playAndRecord, mode: .default, options: options)
    }

    private func configureAudio() {
        let session = AVAudioSession.sharedInstance()
        do {
            if voiceMode {
                try setListeningCategory()
                try session.setActive(true)
                try listener.start()
            } else {
                try session.setCategory(.playback, mode: .spokenAudio)
                try session.setActive(true)
            }
        } catch {
            Log.write("audio setup failed: \(error)", "audio")
            voiceMode = false
            note = "Couldn't start the microphone (\(error.localizedDescription)), so this is tap mode."
            try? session.setCategory(.playback, mode: .spokenAudio)
            try? session.setActive(true)
        }
    }

    /// Leaving the player: remember where we were, release audio and controls.
    /// Called by the X and by swiping the player away; safe to call twice.
    func close() {
        guard !closed else { return }
        closed = true
        persist()
        cancelFlow()
        player.pause()
        if let o = timeObserver { player.removeTimeObserver(o); timeObserver = nil }
        observers.forEach { NotificationCenter.default.removeObserver($0) }
        observers = []
        listener.stop()
        coach.stop()
        let c = MPRemoteCommandCenter.shared()
        for cmd in [c.playCommand, c.pauseCommand, c.togglePlayPauseCommand,
                    c.nextTrackCommand, c.previousTrackCommand, c.changePlaybackPositionCommand] {
            cmd.removeTarget(nil)
        }
        MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
        try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
    }

    /// Save a resume point (and the results so far). Called after every answer,
    /// on pause, every few seconds while playing, and when the app goes away.
    func persist() {
        lastPersist = Date()
        guard phase != .idle, phase != .finished else { return }
        guard position > 5 || !record.items.isEmpty else { return }
        var point = position
        if let d = current, flow != nil || (phase == .paused && resumeDrill != nil) {
            point = d.promptStart      // an interrupted drill is asked again from its cue
        }
        if inRound { point = duration }
        store.saveProgress(SavedProgress(record: record, position: point, savedAt: Date()))
        if !record.items.isEmpty { store.save(record) }
    }

    // MARK: controls

    func togglePause() {
        switch phase {
        case .playing:
            player.pause()
            phase = .paused
            releaseAudioForPause()
        case .listening, .secondTry, .feedback:
            resumeDrill = current
            cancelFlow()
            player.pause()
            phase = .paused
            releaseAudioForPause()
        case .paused:
            resumeFromPause()
        default:
            return
        }
        persist()
        updateNowPlaying()
    }

    /// A call, Siri, or AirPods in call mode taking the audio. iOS deactivates
    /// the session and stops the mic engine; both have to be brought back
    /// before anything plays again.
    private func interrupted(began: Bool, shouldResume: Bool) {
        Log.write("interruption \(began ? "began" : "ended")\(shouldResume ? " (may resume)" : ""), phase \(phase)", "audio")
        if began {
            if phase == .playing || phase == .listening || phase == .secondTry || phase == .feedback {
                pausedByInterruption = true
                togglePause()
            }
        } else if shouldResume, pausedByInterruption, phase == .paused {
            togglePause()
        }
    }

    private func reactivateAudio() {
        do {
            if voiceMode { try setListeningCategory() }
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            Log.write("reactivating audio failed: \(error)", "audio")
        }
        if voiceMode { listener.ensureRunning() }
    }

    /// While paused the app is just a player: the mic is released and the
    /// session drops to plain playback, so AirPods leave call mode and their
    /// next press arrives as "play". reactivateAudio() switches back on resume.
    private func releaseAudioForPause() {
        guard voiceMode else { return }
        listener.releaseMic()
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio)
        } catch {
            Log.write("switching to playback while paused failed: \(error)", "audio")
        }
    }

    private func pauseIfRunning() {
        if phase == .playing || phase == .listening || phase == .secondTry || phase == .feedback {
            togglePause()
        }
    }

    private func resumeFromPause() {
        pausedByInterruption = false
        reactivateAudio()
        if inRound {
            resumeDrill = nil
            startRound()
            return
        }
        guard let d = resumeDrill else {
            phase = .playing
            player.play()
            return
        }
        resumeDrill = nil
        if let k = index(of: d) { next = k }
        relocate(to: d.promptStart, play: true)
    }

    func nextDrill() {
        guard phase != .finished, phase != .idle else { return }
        if inRound {
            roundDone = min(roundDone + 1, roundTotal)
            startRound()
            return
        }
        if seeking { goToDrill(next + 1); return }      // pressed again mid-jump
        let k: Int
        if flow != nil, let c = current, let i = index(of: c) { k = i + 1 }
        else { k = drills.firstIndex { $0.promptStart > position + 0.3 } ?? drills.count }
        goToDrill(k)
    }

    func previousDrill() {
        guard phase != .finished, phase != .idle else { return }
        if inRound {
            roundDone = max(roundDone - 1, 0)
            startRound()
            return
        }
        if seeking { goToDrill(max(next - 1, 0)); return }
        let k: Int
        if flow != nil, let c = current, let i = index(of: c) { k = i - 1 }
        else { k = drills.lastIndex { $0.promptEnd <= position + 0.05 } ?? 0 }
        goToDrill(max(k, 0))
    }

    private func goToDrill(_ k: Int) {
        guard k < drills.count else {
            seek(to: max(duration - 0.3, 0))
            return
        }
        let wasPaused = phase == .paused
        cancelFlow()
        resumeDrill = nil
        let d = drills[k]
        next = k
        current = d
        lastVerdict = nil
        lastHeard = nil
        Log.write("jump to drill \(k + 1)/\(total): \(d.cue)", "player")
        relocate(to: d.promptStart, play: !wasPaused)
    }

    /// Scrubbing, ±10 s and chapter jumps. Not during the second-chance round,
    /// which plays its own short pieces of the episode.
    func seek(to t: Double) {
        guard !inRound, phase != .finished, phase != .idle else { return }
        let wasPaused = phase == .paused
        cancelFlow()
        resumeDrill = nil
        lastVerdict = nil
        lastHeard = nil
        let target = max(0, min(t, duration - 0.1))
        next = firstDrill(endingAfter: target)
        Log.write("seek to \(timeString(target)), next drill \(next + 1)", "player")
        relocate(to: target, play: !wasPaused)
    }

    /// Move the playhead: pause, seek, and only then play (or stay paused). Until
    /// the seek lands, tick() ignores the old position; if another jump comes
    /// in meanwhile, only the latest one takes effect.
    private func relocate(to t: Double, play: Bool) {
        seeking = true
        relocateGen += 1
        let gen = relocateGen
        player.pause()
        Task { [weak self] in
            guard let self else { return }
            await self.seekTo(t)
            guard gen == self.relocateGen else { return }
            self.seeking = false
            self.phase = play ? .playing : .paused
            if play { self.player.play() }
            self.updateNowPlaying()
        }
    }

    func skip(_ seconds: Double) { seek(to: position + seconds) }
    func jump(to chapter: Chapter) { seek(to: chapter.start) }

    /// Correct the automatic verdict — the recogniser sometimes mishears a
    /// right answer, or accepts a wrong one. In tap mode this is how misses are
    /// marked at all.
    func correct(_ v: Verdict) {
        guard !record.items.isEmpty else { return }
        var i = record.items.count - 1
        // While the current drill has no answer yet, the button means the last one.
        if record.items[i].attempts.isEmpty && voiceMode && flow != nil && i > 0 { i -= 1 }
        record.items[i].correction = v
        lastVerdict = v
        tones.play(Cue(v))
        persist()
        if v == .correct, phase == .secondTry || (phase == .listening && attempt == 2) {
            skipRetry()
        }
    }

    /// Go straight to the answer instead of trying a second time.
    func skipRetry() {
        guard let d = current, phase == .secondTry || (phase == .listening && attempt == 2) else { return }
        let round = inRound
        cancelFlow()
        if round {
            roundDone += 1
            startRound()
            return
        }
        lastVerdict = record.items.last?.outcome
        relocate(to: d.answerStart, play: true)
    }

    // MARK: the drill loop

    private func tick(_ t: Double) {
        guard t.isFinite, !seeking else { return }
        position = t
        if let w = waiter, player.rate > 0, t >= w.time - 0.02 {
            waiter = nil
            player.pause()
            w.cont.resume(returning: true)
            return
        }
        guard phase == .playing, flow == nil, !inRound else { return }
        if Date().timeIntervalSince(lastPersist) > 10 { persist() }
        guard next < drills.count else { return }
        let d = drills[next]
        if t >= d.promptEnd - 0.03 {
            next += 1
            startDrill(d)
        }
    }

    private func startDrill(_ d: Drill) {
        current = d
        guard voiceMode else {
            record.items.append(DrillResult(seg: d.id, cue: d.cue, expected: d.expected, attempts: [],
                                            correction: nil, round: 0, chapter: d.chapter))
            lastVerdict = nil
            lastHeard = nil
            persist()
            return
        }
        player.pause()
        flow = Task { [weak self] in
            guard let self else { return }
            await self.drillFlow(d, round: 0)
            if !Task.isCancelled { self.flow = nil }
        }
    }

    /// Ask one drill: up to two listens, the verdict, then the right answer.
    private func drillFlow(_ d: Drill, round: Int) async {
        current = d
        attempt = 1
        liveHeard = nil
        lastHeard = nil
        lastVerdict = nil
        lastHint = nil
        record.items.append(DrillResult(seg: d.id, cue: d.cue, expected: d.expected, attempts: [],
                                        correction: nil, round: round, chapter: d.chapter))
        let idx = record.items.count - 1
        updateNowPlaying()

        for n in 1...2 {
            attempt = n
            if n == 2 {
                phase = .secondTry
                await coach.say(lastVerdict == .noAnswer ? .onceMoreSilence : .onceMoreMiss)
                if Task.isCancelled { return }
                guard await playSpan(from: d.promptStart, to: d.promptEnd) else { return }
                if Task.isCancelled { return }
            }
            phase = .listening
            liveHeard = nil
            tones.play(.yourTurn)
            try? await Task.sleep(nanoseconds: 400_000_000)
            if Task.isCancelled { return }
            let heard = await listener.listen(expected: d.expected, maxSeconds: max(d.thinkSeconds + 1.5, 4)) {
                [weak self] partial in self?.liveHeard = partial
            }
            if Task.isCancelled { return }
            let judgement = Grader.judge(d, heard: heard)
            let score = judgement.score
            let v = judgement.verdict
            record.items[idx].attempts.append(Attempt(heard: heard, score: score, verdict: v, hint: judgement.hint))
            lastHeard = heard
            lastVerdict = v
            lastHint = judgement.hint
            Log.write("drill \(drillLabel) try \(n): heard \(heard.map { "\"\($0)\"" } ?? "nothing") for \"\(d.expected)\" -> \(v.rawValue) (\(String(format: "%.2f", score)))", "drill")
            persist()
            // "Almost" is not retried: the fix is shown and the answer plays.
            if v == .correct || v == .close || record.items[idx].correction != nil { break }
        }

        let outcome = record.items[idx].outcome
        lastVerdict = outcome
        phase = .feedback
        tones.play(Cue(outcome))
        if let line = Coach.Line.verdict(outcome) { await coach.say(line) }
        if Task.isCancelled { return }

        if round == 0 {
            await seekTo(d.answerStart)
            if Task.isCancelled { return }
            phase = .playing
            player.play()
            updateNowPlaying()
        } else {
            _ = await playSpan(from: d.answerStart, to: min(d.answerEnd + 0.3, duration))
        }
    }

    // MARK: the second-chance round

    private func reachedEnd() {
        if let w = waiter {
            waiter = nil
            w.cont.resume(returning: true)
            return
        }
        guard !inRound, phase == .playing else { return }
        beginRound()
    }

    private func beginRound() {
        cancelFlow()
        player.pause()
        guard voiceMode else { finish(); return }
        var latest: [Int: Verdict] = [:]
        for it in record.items where it.round == 0 { latest[it.seg] = it.outcome }
        roundQueue = drills.filter { d in
            guard let v = latest[d.id] else { return false }
            return v != .correct && v != .unmarked
        }
        guard !roundQueue.isEmpty else { finish(); return }
        Log.write("second chance: \(roundQueue.count) drills", "player")
        inRound = true
        roundTotal = roundQueue.count
        roundDone = 0
        startRound(announce: true)
    }

    private func startRound(announce: Bool = false) {
        cancelFlow()
        flow = Task { [weak self] in
            guard let self else { return }
            if announce {
                await self.coach.say(.secondChance)
                if Task.isCancelled { return }
            }
            while self.roundDone < self.roundQueue.count {
                let d = self.roundQueue[self.roundDone]
                self.current = d
                self.lastVerdict = nil
                self.phase = .playing
                guard await self.playSpan(from: d.promptStart, to: d.promptEnd) else { return }
                if Task.isCancelled { return }
                await self.drillFlow(d, round: 1)
                if Task.isCancelled { return }
                self.roundDone += 1
                self.persist()
            }
            self.flow = nil
            self.finish()
        }
    }

    private func finish() {
        guard phase != .finished else { return }
        cancelFlow()
        player.pause()
        inRound = false
        phase = .finished
        current = nil
        record.finished = Date()
        store.save(record)
        store.clearProgress(pack.header.slug)
        listener.stop()
        updateNowPlaying()
        Log.write("finished \(pack.header.slug): \(rightFirstTime)/\(total) right first time, \(record.items.count) results saved", "player")
        Task { [weak self] in
            guard let self else { return }
            await self.coach.say(.episodeDone)
            await self.store.sync()      // results go to the linked Drive folder, if any
        }
    }

    // MARK: helpers

    private func cancelFlow() {
        flow?.cancel()
        flow = nil
        if let w = waiter {
            waiter = nil
            w.cont.resume(returning: false)
        }
        listener.abort()
        coach.stop()
        // A drill that was interrupted before any answer is not a result.
        if voiceMode, let last = record.items.last, last.attempts.isEmpty, last.correction == nil {
            record.items.removeLast()
        }
        liveHeard = nil
    }

    /// Play a stretch of the episode and wait until it has played (true) or the
    /// flow was interrupted (false).
    private func playSpan(from start: Double, to end: Double) async -> Bool {
        await seekTo(start)
        if Task.isCancelled { return false }
        if let w = waiter {
            waiter = nil
            w.cont.resume(returning: false)
        }
        player.play()
        updateNowPlaying()
        return await withCheckedContinuation { (c: CheckedContinuation<Bool, Never>) in
            waiter = (end, c)
        }
    }

    private func seekTo(_ t: Double) async {
        let target = max(0, min(t, duration))
        _ = await player.seek(to: CMTime(seconds: target, preferredTimescale: 600),
                              toleranceBefore: .zero, toleranceAfter: .zero)
        position = target
    }

    private func index(of d: Drill) -> Int? { drills.firstIndex { $0.id == d.id } }

    private func firstDrill(endingAfter t: Double) -> Int {
        drills.firstIndex { $0.promptEnd > t + 0.05 } ?? drills.count
    }

    // MARK: lock screen and headphones

    /// Headphone double-press = next drill, triple-press = previous drill; the
    /// lock screen gets the same, plus a scrubber.
    private func setupRemoteCommands() {
        let c = MPRemoteCommandCenter.shared()
        c.togglePlayPauseCommand.addTarget { [weak self] _ in
            Log.write("remote: play/pause", "audio")
            Task { @MainActor in self?.togglePause() }
            return .success
        }
        c.playCommand.addTarget { [weak self] _ in
            Log.write("remote: play", "audio")
            Task { @MainActor in if self?.phase == .paused { self?.togglePause() } }
            return .success
        }
        c.pauseCommand.addTarget { [weak self] _ in
            Log.write("remote: pause", "audio")
            Task { @MainActor in self?.pauseIfRunning() }
            return .success
        }
        c.nextTrackCommand.addTarget { [weak self] _ in
            Log.write("remote: next", "audio")
            Task { @MainActor in self?.nextDrill() }
            return .success
        }
        c.previousTrackCommand.addTarget { [weak self] _ in
            Log.write("remote: previous", "audio")
            Task { @MainActor in self?.previousDrill() }
            return .success
        }
        c.changePlaybackPositionCommand.addTarget { [weak self] event in
            let t = (event as? MPChangePlaybackPositionCommandEvent)?.positionTime
            Task { @MainActor in if let t { self?.seek(to: t) } }
            return .success
        }
    }

    private func updateNowPlaying() {
        var info: [String: Any] = [
            MPMediaItemPropertyTitle: pack.header.title,
            MPMediaItemPropertyArtist: "Vorbește · \(drillLabel)",
            MPMediaItemPropertyPlaybackDuration: duration,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: position,
            MPNowPlayingInfoPropertyPlaybackRate: phase == .playing ? 1.0 : 0.0,
        ]
        if let c = currentChapter { info[MPMediaItemPropertyAlbumTitle] = c.name }
        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }
}
