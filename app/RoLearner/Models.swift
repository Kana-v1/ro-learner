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
    /// On an answer: other fully correct phrasings, and understandable ones that
    /// still deserve a correction. Written by the episode builders; absent in
    /// older packs.
    let accept: [String]?
    let almost: [String]?
}

struct PackHeader: Codable {
    let format: Int
    let slug: String
    let title: String
    let lesson: Int
    let duration: Double
    let segments: [PackSegment]
}

/// A drill is an English cue immediately followed by its Romanian answer. The
/// stops come from the episode script (every ep.drill() in the builders), not
/// from listening to the audio.
struct Drill: Identifiable, Equatable {
    let id: Int               // index of the cue segment
    let cue: String
    let expected: String
    let promptStart: Double
    let promptEnd: Double
    let answerStart: Double
    let answerEnd: Double
    let thinkSeconds: Double  // the pause the episode was designed with
    let chapter: String?
    var accept: [String] = []
    var almost: [String] = []
}

struct Chapter: Identifiable {
    let id: Int
    let name: String
    let start: Double
    let drillCount: Int
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
                             chapter: chapter,
                             accept: a.accept ?? [], almost: a.almost ?? []))
        }
        return out
    }

    var chapters: [Chapter] {
        let marks = segments.compactMap { s in s.chapter.map { (name: $0, start: s.start) } }
        let ds = drills
        return marks.enumerated().map { k, m in
            let end = k + 1 < marks.count ? marks[k + 1].start : .infinity
            let count = ds.filter { $0.promptStart >= m.start && $0.promptStart < end }.count
            return Chapter(id: k, name: m.name, start: m.start, drillCount: count)
        }
    }
}

enum Verdict: String, Codable, Hashable {
    case correct, close, missed
    case noAnswer = "no_answer"
    case unmarked             // tap mode: nobody said it was wrong
}

/// Something the learner wants Claude to know — a wrong answer in an episode,
/// a word the app never hears, an idea — with where they were when they said it.
struct FeedbackNote: Codable, Identifiable {
    struct Drill: Codable {
        var seg: Int
        var cue: String
        var expected: String
        var heard: [String]
    }

    var id: String
    var created: Date
    var kind: String              // "wrong_answer", "not_heard", "audio", "idea", "other"
    var text: String
    var episode: String?
    var position: Double?         // playhead, seconds
    var drill: String?            // "41/84", or "second chance 3/12"
    var current: Drill?           // the drill on screen
    var recent: [Drill] = []      // the last few answered, newest last
    var app: String
}

struct Attempt: Codable {
    var heard: String?
    var score: Double
    var verdict: Verdict
    var hint: String?         // for "almost": what to fix
    /// Whether the mic heard a voice, whatever the recogniser made of it: a
    /// no-answer with a voice is the recogniser's miss, not the learner's.
    var voiced: Bool? = nil
    /// Which recogniser this was graded on ("whisper" or "apple"), and when
    /// Whisper was used, what Apple's recogniser made of the same answer —
    /// so the two can be compared from real sessions.
    var engine: String? = nil
    var other: OtherHearing? = nil
}

struct OtherHearing: Codable {
    var engine: String
    var heard: String?
    var verdict: Verdict
}

/// One drill as the learner met it: up to two spoken attempts, and an optional
/// correction when the recogniser misjudged.
struct DrillResult: Codable, Identifiable {
    var id: String { "\(seg)-\(round)" }
    let seg: Int
    let cue: String
    let expected: String
    var attempts: [Attempt]
    var correction: Verdict?
    let round: Int            // 0 = in the episode, 1 = the end-of-episode second chance
    let chapter: String?

    var outcome: Verdict { correction ?? attempts.last?.verdict ?? .unmarked }
    var heard: String? { attempts.last?.heard }
    var rightFirstTime: Bool { attempts.count <= 1 && outcome == .correct }
}

/// One listen-through of one episode. Saved after every drill so a session cut
/// short still counts; exported to Google Drive for Claude to read.
struct SessionRecord: Codable {
    let episode: String
    let title: String
    let started: Date
    var finished: Date?
    var mode: String          // "voice" or "tap"
    var items: [DrillResult]

    /// Stable id shared with ingest_results.py: episode + start time in whole
    /// seconds (the precision the ISO-8601 results file keeps).
    var key: String { "\(episode)_\(Int(started.timeIntervalSince1970))" }
    var mainItems: [DrillResult] { items.filter { $0.round == 0 } }
    var rightFirstTime: Int { mainItems.filter(\.rightFirstTime).count }
}

/// Where an unfinished episode stopped, so it can pick up there.
struct SavedProgress: Codable {
    var record: SessionRecord
    var position: Double
    var savedAt: Date
}

/// Written by Claude after reading a batch of results (ingest_results.py
/// --note); imported like a lesson file. Marks those sessions analysed and
/// carries a short written report.
struct AnalysisNote: Codable {
    let format: Int
    let created: Date
    let analyzed: [String]
    let report: String?
}

/// Each session's way to Claude. Kept on the phone.
struct AnalysisStatus: Codable {
    var sent: [String: Date] = [:]        // session key -> when it was uploaded
    var analyzed: Set<String> = []
    var pulled: [String: Date] = [:]      // Drive file ("lessons/x.rolesson") -> version imported
}
