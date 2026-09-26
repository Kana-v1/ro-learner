import AVFoundation

/// What the learner hears besides the episode, so the app works from a pocket:
/// a rising chime when it is their turn, a tone per verdict, and a few short
/// spoken prompts. English only — the course never has an English voice speak
/// Romanian.
enum Cue: Hashable {
    case yourTurn, right, notQuite, noAnswer

    init(_ v: Verdict) {
        switch v {
        case .correct: self = .right
        case .close, .missed: self = .notQuite
        case .noAnswer, .unmarked: self = .noAnswer
        }
    }
}

/// Short tones, synthesised once at start-up so nothing needs bundling.
final class Tones {
    private var players: [Cue: AVAudioPlayer] = [:]

    init() {
        players[.yourTurn] = Self.make([523, 659, 784], note: 0.09)
        players[.right] = Self.make([880, 1320], note: 0.11)
        players[.notQuite] = Self.make([392, 294], note: 0.13)
        players[.noAnswer] = Self.make([262], note: 0.18)
    }

    func play(_ cue: Cue) {
        guard let p = players[cue] else { return }
        p.currentTime = 0
        p.play()
    }

    private static func make(_ freqs: [Double], note: Double) -> AVAudioPlayer? {
        let rate = 44100.0
        var samples: [Int16] = []
        for f in freqs {
            let n = Int(rate * note)
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

/// Speaks a short English prompt and lets the caller wait until it has finished,
/// so a prompt never talks over the episode or the learner's turn.
@MainActor
final class Announcer: NSObject, AVSpeechSynthesizerDelegate {
    private let synth = AVSpeechSynthesizer()
    private var pending: CheckedContinuation<Void, Never>?

    /// The highest-quality US English voice installed (enhanced or premium if
    /// the user has downloaded one), not the compact default.
    private static let bestVoice: AVSpeechSynthesisVoice? =
        AVSpeechSynthesisVoice.speechVoices()
            .filter { $0.language == "en-US" }
            .max { $0.quality.rawValue < $1.quality.rawValue }
        ?? AVSpeechSynthesisVoice(language: "en-US")
    private var speaking: ObjectIdentifier?

    override init() {
        super.init()
        synth.delegate = self
    }

    func say(_ text: String) async {
        finishPending()
        guard !text.isEmpty else { return }
        let u = AVSpeechUtterance(string: text)
        u.voice = Self.bestVoice
        speaking = ObjectIdentifier(u)
        await withCheckedContinuation { (c: CheckedContinuation<Void, Never>) in
            pending = c
            synth.speak(u)
        }
    }

    func stop() {
        synth.stopSpeaking(at: .immediate)
        finishPending()
    }

    private func finishPending() {
        speaking = nil
        let c = pending
        pending = nil
        c?.resume()
    }

    private func done(_ id: ObjectIdentifier) {
        // A late callback for an utterance that was already cut off must not
        // release the wait of the one that replaced it.
        guard id == speaking else { return }
        finishPending()
    }

    nonisolated func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        let id = ObjectIdentifier(utterance)
        Task { @MainActor in self.done(id) }
    }

    nonisolated func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        let id = ObjectIdentifier(utterance)
        Task { @MainActor in self.done(id) }
    }
}
