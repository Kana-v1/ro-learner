import Foundation

/// One segment of an episode, with its exact position in the pack's audio.
/// Written by make_lesson_pack.py; times are sample-exact, not estimates.
struct PackSegment: Codable {
    let i: Int
    let type: String          // narration, target, gloss, prompt, answer, line_*
    let lang: String
    let text: String
    let start: Double
    let end: Double           // end of speech; the designed pause follows
    let pause: Int            // ms of silence after this segment
    let voice: String
    let chapter: String?
}

struct PackHeader: Codable {
    let format: Int
    let slug: String
    let title: String
    let lesson: Int
    let duration: Double
    let segments: [PackSegment]
}

/// A drill is an English cue immediately followed by its Romanian answer.
/// The player stops at `promptEnd`, listens, then plays from `answerStart`.
struct Drill: Identifiable {
    let id: Int               // index of the cue segment
    let cue: String
    let expected: String
    let promptStart: Double
    let promptEnd: Double
    let answerStart: Double
    let answerEnd: Double
    let thinkSeconds: Double  // the pause the episode was designed with
    let chapter: String?
}

extension PackHeader {
    var drills: [Drill] {
        var out: [Drill] = []
        var chapter: String?
        for (k, s) in segments.enumerated() {
            if let c = s.chapter { chapter = c }
            guard s.type == "prompt", k + 1 < segments.count,
                  segments[k + 1].type == "answer" else { continue }
            let a = segments[k + 1]
            out.append(Drill(id: s.i, cue: s.text, expected: a.text,
                             promptStart: s.start, promptEnd: s.end,
                             answerStart: a.start, answerEnd: a.end,
                             thinkSeconds: Double(s.pause) / 1000,
                             chapter: chapter))
        }
        return out
    }
}

enum Verdict: String, Codable, Hashable {
    case correct, close, missed
    case noAnswer = "no_answer"
    case unmarked             // tap mode: nobody said it was wrong
}

struct DrillResult: Codable, Identifiable {
    var id: String { "\(seg)-\(retry)" }
    let seg: Int
    let cue: String
    let expected: String
    var heard: String?
    var score: Double
    var verdict: Verdict
    var overridden: Bool      // the learner corrected the automatic verdict
    let retry: Bool           // asked again in the "second chance" round
    let chapter: String?
}

/// One listen-through of one episode. Saved after every drill so a session cut
/// short still counts; exported to Google Drive for the course to adapt to.
struct SessionRecord: Codable {
    let episode: String
    let title: String
    let started: Date
    var finished: Date?
    var mode: String          // "voice" or "tap"
    var items: [DrillResult]
}
