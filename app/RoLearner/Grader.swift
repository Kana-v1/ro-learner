import Foundation

/// Compares what the recogniser heard with the expected answer, word by word.
///
/// Lenient where the recogniser or real speech differ from the script, strict
/// where the learner could actually be wrong:
/// - diacritics are folded (the recogniser is inconsistent with ă/â/î/ș/ț, and
///   agreement endings still differ in letters: alb / albă / albi / albe)
/// - a subject pronoun the learner dropped is not required — Romanian is
///   pro-drop and the dialogue teaches exactly that
/// - este and e count as the same word
enum Grader {
    static let optionalPronouns: Set<String> = ["eu", "tu", "el", "ea", "noi", "voi", "ei", "ele"]

    static func tokens(_ s: String) -> [String] {
        let normalised = s.lowercased()
            .replacingOccurrences(of: "ş", with: "ș")
            .replacingOccurrences(of: "ţ", with: "ț")
        var spaced = ""
        for ch in normalised { spaced.append(ch.isLetter ? ch : " ") }
        return spaced.split(separator: " ").map { word in
            let folded = String(word).folding(options: .diacriticInsensitive, locale: nil)
            return folded == "este" ? "e" : folded
        }
    }

    /// 0...1. Mostly recall of the expected words (in order), with a small
    /// penalty for extra words so rambling past the answer is not full marks.
    static func score(expected: String, heard: String) -> Double {
        let h = tokens(heard)
        let e = tokens(expected).filter { !optionalPronouns.contains($0) || h.contains($0) }
        guard !e.isEmpty, !h.isEmpty else { return 0 }

        var dp = Array(repeating: Array(repeating: 0, count: h.count + 1), count: e.count + 1)
        for i in 1...e.count {
            for j in 1...h.count {
                dp[i][j] = e[i - 1] == h[j - 1] ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1])
            }
        }
        let common = Double(dp[e.count][h.count])
        let recall = common / Double(e.count)
        let precision = common / Double(h.count)
        return recall * (0.8 + 0.2 * precision)
    }

    static func verdict(score: Double, heard: String?) -> Verdict {
        guard let heard, !tokens(heard).isEmpty else { return .noAnswer }
        if score >= 0.85 { return .correct }
        if score >= 0.5 { return .close }
        return .missed
    }
}
