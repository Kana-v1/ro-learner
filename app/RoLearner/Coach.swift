import AVFoundation

/// The app's guide voice. Its few phrases are rendered once with a natural Azure
/// voice (tools/make_coach_voice.py) and bundled as mp3s, so it sounds like a
/// person rather than iOS's built-in speech, and every phrase has an exact
/// length: the episode only resumes after the phrase (plus a breath) is over.
/// A phrase that has not been rendered yet falls back to the best installed
/// system voice. English only — Romanian is only ever spoken by the episode.
@MainActor
final class Coach {
    /// Raw values are the mp3 file names; keep in step with PHRASES in
    /// tools/make_coach_voice.py.
    enum Line: String, CaseIterable {
        case right1 = "right_1", right2 = "right_2", right3 = "right_3"
        case almost
        case notQuite = "not_quite"
        case noAnswer = "no_answer"
        case onceMoreMiss = "once_more_miss"
        case onceMoreSilence = "once_more_silence"
        case secondChance = "second_chance"
        case episodeDone = "episode_done"

        var text: String {
            switch self {
            case .right1: return "Right."
            case .right2: return "That's it."
            case .right3: return "Good."
            case .almost: return "Almost."
            case .notQuite: return "Not quite."
            case .noAnswer: return "I didn't catch that."
            case .onceMoreMiss: return "Not quite. Once more."
            case .onceMoreSilence: return "I didn't catch that. Try once more."
            case .secondChance: return "Second chance. Let's go over the ones you missed."
            case .episodeDone: return "That's the episode. Nice work."
            }
        }

        static func verdict(_ v: Verdict) -> Line? {
            switch v {
            case .correct: return [.right1, .right2, .right3].randomElement()
            case .close: return .almost
            case .missed: return .notQuite
            case .noAnswer: return .noAnswer
            case .unmarked: return nil
            }
        }
    }

    private var clips: [Line: AVAudioPlayer] = [:]
    private var playing: AVAudioPlayer?
    private let fallback = Announcer()

    init() {
        for line in Line.allCases {
            if let url = Bundle.main.url(forResource: line.rawValue, withExtension: "mp3"),
               let p = try? AVAudioPlayer(contentsOf: url) {
                p.prepareToPlay()
                clips[line] = p
            }
        }
        Log.write("coach voice: \(clips.count) of \(Line.allCases.count) phrases bundled", "audio")
    }

    /// Say a line; returns once it has finished, with a short breath after, so
    /// nothing that follows can talk over it.
    func say(_ line: Line) async {
        guard let p = clips[line] else {
            await fallback.say(line.text)
            try? await Task.sleep(nanoseconds: 400_000_000)
            return
        }
        playing?.stop()
        p.currentTime = 0
        p.play()
        playing = p
        try? await Task.sleep(nanoseconds: UInt64((p.duration + 0.35) * 1_000_000_000))
        if Task.isCancelled { p.stop() }
    }

    func stop() {
        playing?.stop()
        playing = nil
        fallback.stop()
    }
}
