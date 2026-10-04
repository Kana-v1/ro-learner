import Foundation

/// Judges what the recogniser heard against a drill's answers.
///
/// Three outcomes, because "not the exact sentence" is not the same as wrong:
///
/// - **right**: every word of the answer, or of one of the drill's accepted
///   alternatives (`accept`, written into the episode when it is generated).
/// - **almost**: the meaning is there but something needs correcting — a
///   small word left out (un, o, niște, e), one word with the right stem but
///   the wrong ending (alb for albă: in Romanian that ending *is* the grammar,
///   so it is never silently accepted), or a phrasing the episode marked as
///   understandable-but-not-the-lesson (`almost`). No retry: the learner is
///   told the fix and hears the answer.
/// - **not quite**: a content word missing or different. This gets a retry.
///
/// One extra word is not ignored: un/o slipped in between the answer's words
/// (e un medic for e medic). English puts an article before a profession and
/// Romanian doesn't, and the learner does it every time, so it is an almost.
///
/// Lenient where the recogniser or real speech differ from the script:
/// diacritics are folded (the recogniser is inconsistent with ă/â/î/ș/ț, and
/// can't hear sora from soră anyway), a subject pronoun the learner dropped
/// is not required (Romanian is pro-drop), este and e are the same word, and
/// extra words around the answer are ignored.
enum Grader {
    struct Judgement {
        let verdict: Verdict
        let score: Double         // 0...1, for the log and results
        let hint: String?         // what to fix, for an "almost"
    }

    static let optionalPronouns: Set<String> = ["eu", "tu", "el", "ea", "noi", "voi", "ei", "ele"]
    /// Words the recogniser often drops and whose absence is a slip, not a
    /// wrong answer.
    static let smallWords: Set<String> = ["un", "o", "niste", "e"]

    /// (folded form for comparing, original form for showing)
    static func words(_ s: String) -> [(key: String, shown: String)] {
        let normalised = s
            .replacingOccurrences(of: "ş", with: "ș").replacingOccurrences(of: "ţ", with: "ț")
            .replacingOccurrences(of: "Ş", with: "Ș").replacingOccurrences(of: "Ţ", with: "Ț")
        var spaced = ""
        for ch in normalised { spaced.append(ch.isLetter ? ch : " ") }
        return spaced.split(separator: " ").map { w in
            let shown = String(w)
            let folded = shown.lowercased().folding(options: .diacriticInsensitive, locale: nil)
            return (key: folded == "este" ? "e" : folded, shown: shown.lowercased())
        }
    }

    static func tokens(_ s: String) -> [String] { words(s).map(\.key) }

    static func judge(_ d: Drill, heard: String?) -> Judgement {
        guard let heard, !tokens(heard).isEmpty else {
            return Judgement(verdict: .noAnswer, score: 0, hint: nil)
        }
        var best = compare(expected: d.expected, heard: heard)
        for alt in d.accept {
            let j = compare(expected: alt, heard: heard)
            if rank(j.verdict) > rank(best.verdict) || (j.verdict == best.verdict && j.score > best.score) {
                best = j
            }
        }
        // An understandable phrasing the episode flagged: say it the lesson's way.
        if best.verdict != .correct {
            for alt in d.almost where compare(expected: alt, heard: heard).verdict == .correct {
                return Judgement(verdict: .close, score: 0.8, hint: "Say it as the lesson does: \(d.expected)")
            }
        }
        return best
    }

    /// Grade the recogniser's ranked guesses. Its best guess counts as is; a
    /// lower-ranked guess can lift the verdict by at most one level. The
    /// expected answer is hinted to the recogniser, so a low-ranked guess can
    /// "hear" it when something else was said — enough to rescue a
    /// misrecognition (almost -> right), not to turn a miss into a pass.
    static func judgeBest(_ d: Drill, guesses: [String]) -> (judgement: Judgement, heard: String?, used: Int) {
        guard let top = guesses.first else { return (judge(d, heard: nil), nil, 0) }
        let topJudgement = judge(d, heard: top)
        var best = (judgement: topJudgement, heard: Optional(top), used: 0)
        for (k, g) in guesses.enumerated().dropFirst() {
            let j = judge(d, heard: g)
            let capped = min(rank(j.verdict), rank(topJudgement.verdict) + 1)
            if capped > rank(best.judgement.verdict) {
                let v: Verdict = capped == rank(j.verdict) ? j.verdict : .close
                let hint = v == j.verdict ? j.hint : "Heard you as “\(top)”; say it clearly: \(d.expected)"
                best = (Judgement(verdict: v, score: j.score, hint: hint), g, k)
            }
        }
        return best
    }

    private static func rank(_ v: Verdict) -> Int {
        switch v {
        case .correct: return 3
        case .close: return 2
        case .missed: return 1
        case .noAnswer, .unmarked: return 0
        }
    }

    /// Align the answer's words with what was heard, allowing a word to match
    /// exactly (2) or by stem with a different ending (1), and classify each
    /// answer word as exact, near, or missing.
    static func compare(expected: String, heard: String) -> Judgement {
        var h = words(heard)
        let hKeys = Set(h.map(\.key))
        let e = words(expected).filter { !optionalPronouns.contains($0.key) || hKeys.contains($0.key) }
        guard !e.isEmpty else { return Judgement(verdict: .missed, score: 0, hint: nil) }
        // The recogniser clips the last consonants of the last word — the
        // release of a final g, c, k is quiet ("La" for larg, "mi" for mic).
        // When the heard last word is the answer's last word minus consonants
        // only, it is that word. A missing vowel is not clipping: lung/lungă
        // and bun/bună stay different.
        if let lastH = h.last, let lastE = e.last, lastH.key != lastE.key, lastH.key.count >= 2,
           lastE.key.hasPrefix(lastH.key),
           lastE.key.dropFirst(lastH.key.count).allSatisfy({ !"aeiou".contains($0) }) {
            h[h.count - 1] = lastE
        }

        let n = e.count, m = h.count
        var dp = Array(repeating: Array(repeating: 0, count: m + 1), count: n + 1)
        for i in 1...n {
            for j in 1...m {
                let w = e[i - 1].key == h[j - 1].key ? 2 : (sameStem(e[i - 1].key, h[j - 1].key) ? 1 : 0)
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], w > 0 ? dp[i - 1][j - 1] + w : 0)
            }
        }
        // walk back to see what happened to each answer word
        var near: [(want: String, got: String)] = []
        var missing: [(key: String, shown: String)] = []
        var alignedTo = Array(repeating: -1, count: m)     // heard word -> answer word
        var i = n, j = m
        while i > 0 {
            if j > 0 {
                let w = e[i - 1].key == h[j - 1].key ? 2 : (sameStem(e[i - 1].key, h[j - 1].key) ? 1 : 0)
                if w > 0 && dp[i][j] == dp[i - 1][j - 1] + w {
                    if w == 1 { near.append((want: e[i - 1].shown, got: h[j - 1].shown)) }
                    alignedTo[j - 1] = i - 1
                    i -= 1; j -= 1
                    continue
                }
                if dp[i][j] == dp[i][j - 1] { j -= 1; continue }
            }
            missing.append(e[i - 1])
            i -= 1
        }

        let missingSmall = missing.filter { smallWords.contains($0.key) }
        let missingContent = missing.filter { !smallWords.contains($0.key) }
        let score = Double(dp[n][m]) / Double(2 * n)

        // un/o heard between two consecutive answer words
        let articles: Set<String> = ["un", "o"]
        let inserted = (1..<max(m - 1, 1)).first { j in
            articles.contains(h[j].key) && alignedTo[j] < 0 && alignedTo[j - 1] >= 0
                && alignedTo[j + 1] == alignedTo[j - 1] + 1
        }
        let insertedHint = inserted.map { "No \(h[$0].shown) before \(e[alignedTo[$0 + 1]].shown)" }

        if missing.isEmpty && near.isEmpty {
            if let insertedHint { return Judgement(verdict: .close, score: 0.9, hint: insertedHint) }
            return Judgement(verdict: .correct, score: 1, hint: nil)
        }
        if missingContent.isEmpty && near.count <= 1 {
            var parts: [String] = []
            if !missingSmall.isEmpty {
                // A small word said in place of the right one is usually the
                // gender slip these lessons drill (un soră for o soră).
                let expectedSmall = Set(e.map(\.key)).intersection(smallWords)
                let wrongSmall = h.filter { smallWords.contains($0.key) && !expectedSmall.contains($0.key) }
                let want = missingSmall.reversed().map(\.shown).joined(separator: ", ")
                if let said = wrongSmall.first {
                    parts.append("Say \(want), not \(said.shown)")
                } else {
                    parts.append("Left out: \(want)")
                }
            }
            if let x = near.first {
                parts.append("Check the ending: \(x.want) (heard \(x.got))")
            }
            if let insertedHint { parts.append(insertedHint) }
            return Judgement(verdict: .close, score: score, hint: parts.joined(separator: " · "))
        }
        return Judgement(verdict: .missed, score: score, hint: nil)
    }

    /// Same word, different ending — judged relative to the words' length, not
    /// by fixed letter counts, so short words and long ones are treated alike:
    /// - both at least 2 letters (a floor, so the article o is never a "near"
    ///   un),
    /// - they share a start of at least half the shorter word (and never
    ///   fewer than 2 letters): the stem,
    /// - and differ by at most 40% of the longer word (edit distance).
    /// alb/albă, bun/bună, negri/negre, profesor/profesoară are near;
    /// soră/sare, am/ai, mama/tata are not.
    static func sameStem(_ a: String, _ b: String) -> Bool {
        guard a != b else { return false }
        let x = Array(a), y = Array(b)
        let shorter = min(x.count, y.count), longer = max(x.count, y.count)
        guard shorter >= 2 else { return false }
        var k = 0
        while k < shorter && x[k] == y[k] { k += 1 }
        guard k >= max(2, (shorter + 1) / 2) else { return false }
        return Double(editDistance(x, y)) <= 0.4 * Double(longer)
    }

    static func editDistance(_ x: [Character], _ y: [Character]) -> Int {
        var prev = Array(0...y.count)
        for i in 1...max(x.count, 1) where !x.isEmpty {
            var row = [i] + Array(repeating: 0, count: y.count)
            for j in 1...max(y.count, 1) where !y.isEmpty {
                row[j] = min(prev[j] + 1, row[j - 1] + 1, prev[j - 1] + (x[i - 1] == y[j - 1] ? 0 : 1))
            }
            prev = row
        }
        return x.isEmpty ? y.count : prev[y.count]
    }
}
