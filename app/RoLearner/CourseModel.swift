import Foundation
import Speech

/// A language model trained on the course's own answers, for on-device
/// recognition (Settings → Recognition → Tuned to the course).
///
/// A general recogniser has to guess among every word of Romanian, and a
/// short word said on its own — mic, lung, larg — has almost no context to
/// guess from, so it comes back as nothing or as a commoner word. Here the
/// set of things the learner will say is known in advance: every drill's
/// answer and its accepted phrasings. Apple's way of telling the recogniser
/// that is a custom language model (SFCustomLanguageModelData, iOS 17), which
/// only works on-device. Its weights: each whole answer counts most, then the
/// accepted and almost-right phrasings, then each word alone — so a bare word
/// drill is as expected as a sentence.
///
/// Built once per change in the set of episodes, in the background; until it
/// is ready (or if this phone can't build one for Romanian) recognition uses
/// the servers, and the log says why.
@MainActor
final class CourseModel {
    static let shared = CourseModel()

    private(set) var configuration: SFSpeechLanguageModel.Configuration?
    private(set) var status = "not built"
    private var building: Task<Void, Never>?
    private var builtKey: String?

    private let dir = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        .appendingPathComponent("CourseModel", isDirectory: true)

    /// (Re)build for these episodes if their answers changed since last time.
    func update(packs: [Pack]) {
        var counts: [String: Int] = [:]
        func add(_ phrase: String, _ n: Int) {
            let p = Self.clean(phrase)
            if !p.isEmpty { counts[p, default: 0] += n }
        }
        for pack in packs {
            for d in pack.header.drills {
                add(d.expected, 10)
                d.accept.forEach { add($0, 6) }
                d.almost.forEach { add($0, 3) }
                for w in Grader.words(d.expected).map(\.shown) where w.count >= 2 { add(w, 4) }
            }
        }
        guard !counts.isEmpty else { return }
        // Same answers as the model already on disk: just use it.
        let key = Self.stableHash(counts.keys.sorted().joined(separator: "|")) + "-\(counts.count)"
        guard key != builtKey, building == nil else { return }
        let files = paths(for: key)
        if FileManager.default.fileExists(atPath: files.model.path),
           UserDefaults.standard.string(forKey: "courseModelKey") == key {
            configuration = SFSpeechLanguageModel.Configuration(languageModel: files.model,
                                                                vocabulary: files.vocabulary)
            builtKey = key
            status = "ready (\(counts.count) phrases)"
            return
        }
        status = "building (\(counts.count) phrases)"
        building = Task { [weak self] in
            await self?.build(counts: counts, key: key, files: files)
            self?.building = nil
        }
    }

    private func paths(for key: String) -> (data: URL, model: URL, vocabulary: URL) {
        let d = dir.appendingPathComponent(key, isDirectory: true)
        return (d.appendingPathComponent("training.bin"), d.appendingPathComponent("model.lm"),
                d.appendingPathComponent("vocabulary.voc"))
    }

    private func build(counts: [String: Int], key: String,
                       files: (data: URL, model: URL, vocabulary: URL)) async {
        let started = Date()
        do {
            try? FileManager.default.removeItem(at: dir)          // old models
            try FileManager.default.createDirectory(at: files.data.deletingLastPathComponent(),
                                                    withIntermediateDirectories: true)
            let data = SFCustomLanguageModelData(locale: Locale(identifier: "ro-RO"),
                                                 identifier: "io.github.kanav1.rolearner.course",
                                                 version: key)
            for (phrase, n) in counts {
                data.insert(phraseCount: SFCustomLanguageModelData.PhraseCount(phrase: phrase, count: n))
            }
            try await data.export(to: files.data)
            let config = SFSpeechLanguageModel.Configuration(languageModel: files.model,
                                                             vocabulary: files.vocabulary)
            // The clientIdentifier form: the only one in the iOS 18 SDK the CI
            // builds with (deprecated in iOS 26, still working).
            try await SFSpeechLanguageModel.prepareCustomLanguageModel(
                for: files.data, clientIdentifier: "io.github.kanav1.rolearner", configuration: config)
            configuration = config
            builtKey = key
            UserDefaults.standard.set(key, forKey: "courseModelKey")
            status = "ready (\(counts.count) phrases)"
            Log.write("course model built: \(counts.count) phrases in \(String(format: "%.1f", Date().timeIntervalSince(started))) s", "speech")
        } catch {
            configuration = nil
            builtKey = key          // don't retry the same set over and over
            status = "failed: \(error.localizedDescription)"
            Log.write("course model failed: \(error)", "speech")
        }
    }

    /// FNV-1a: unlike hashValue, the same across launches.
    private static func stableHash(_ s: String) -> String {
        var h: UInt64 = 0xcbf29ce484222325
        for byte in s.utf8 { h = (h ^ UInt64(byte)) &* 0x100000001b3 }
        return String(h, radix: 36)
    }

    /// Phrases as the recogniser should see them: comma-below ș/ț, no
    /// punctuation, single spaces.
    private static func clean(_ s: String) -> String {
        let t = s.replacingOccurrences(of: "ş", with: "ș").replacingOccurrences(of: "ţ", with: "ț")
            .replacingOccurrences(of: "Ş", with: "Ș").replacingOccurrences(of: "Ţ", with: "Ț")
        var out = ""
        for ch in t { out.append(ch.isLetter || ch == "'" ? ch : " ") }
        return out.split(separator: " ").joined(separator: " ")
    }
}
