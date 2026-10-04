import Foundation

/// Two-way sync with a folder the learner linked once (normally in Google
/// Drive, reached through the Files app):
///
///     <folder>/lessons/*.rolesson     pulled: new episodes, put there by the course scripts
///     <folder>/notes/*.roanalysis     pulled: Claude's notes on the results
///     <folder>/results/<key>.json     pushed: one file per finished session
///
/// iOS only lets an app touch another app's files while it is open, so this runs
/// when the app comes to the foreground, after an episode ends, and on
/// pull-to-refresh. Everything goes through NSFileCoordinator so the Drive app
/// downloads (and uploads) the files on demand. It is blocking file I/O, so it
/// runs off the main actor; the store imports what it brings back.
enum DriveSync {
    struct Outgoing: Sendable {
        let key: String
        let fileName: String
        let data: Data
        var folder = "results"        // or "feedback"
    }

    struct Pulled: Sendable {
        let name: String          // "lessons/episode_06a.rolesson"
        let modified: Date
        let local: URL            // a copy in the app's temporary folder
    }

    struct Outcome: Sendable {
        var lessons: [Pulled] = []
        var notes: [Pulled] = []
        var pushed: [String] = []
        var problem: String?
    }

    static func run(root: URL, known: [String: Date], outgoing: [Outgoing], log: Data? = nil) -> Outcome {
        var outcome = Outcome()
        let scoped = root.startAccessingSecurityScopedResource()
        defer { if scoped { root.stopAccessingSecurityScopedResource() } }

        let fm = FileManager.default
        let coordinator = NSFileCoordinator()
        let tmp = fm.temporaryDirectory.appendingPathComponent("drive-pull", isDirectory: true)
        try? fm.createDirectory(at: tmp, withIntermediateDirectories: true)

        Log.write("sync: folder \(root.path) (scoped access: \(scoped))", "drive")

        /// `sub` "" means the linked folder itself: lessons dropped straight in,
        /// or a lessons folder linked directly, are found too.
        func pull(_ sub: String, ext: String) -> [Pulled] {
            let dir = sub.isEmpty ? root : root.appendingPathComponent(sub, isDirectory: true)
            var items: [URL] = []
            var listError: NSError?
            var innerError: Error?
            coordinator.coordinate(readingItemAt: dir, options: [], error: &listError) { url in
                do {
                    items = try fm.contentsOfDirectory(
                        at: url, includingPropertiesForKeys: [.contentModificationDateKey],
                        options: [.skipsHiddenFiles])
                } catch {
                    innerError = error
                }
            }
            let label = sub.isEmpty ? "(folder itself)" : sub
            if let e = listError ?? innerError.map({ $0 as NSError }) {
                if !(e.domain == NSCocoaErrorDomain && e.code == NSFileReadNoSuchFileError) {
                    Log.write("list \(label) failed: \(e.domain) \(e.code) \(e.localizedDescription)", "drive")
                }
            } else {
                Log.write("list \(label): \(items.count) item(s), \(items.filter { $0.pathExtension == ext }.count) .\(ext)", "drive")
            }
            var found: [Pulled] = []
            for item in items where item.pathExtension == ext {
                let name = sub.isEmpty ? item.lastPathComponent : "\(sub)/\(item.lastPathComponent)"
                let modified = (try? item.resourceValues(forKeys: [.contentModificationDateKey]))?
                    .contentModificationDate ?? .distantPast
                if let seen = known[name], seen >= modified { continue }
                var readError: NSError?
                coordinator.coordinate(readingItemAt: item, options: [.withoutChanges], error: &readError) { url in
                    let dest = tmp.appendingPathComponent(item.lastPathComponent)
                    try? fm.removeItem(at: dest)
                    if (try? fm.copyItem(at: url, to: dest)) != nil {
                        found.append(Pulled(name: name, modified: modified, local: dest))
                    }
                }
                if let readError {
                    outcome.problem = readError.localizedDescription
                    Log.write("read \(name) failed: \(readError.domain) \(readError.code) \(readError.localizedDescription)", "drive")
                } else {
                    Log.write("pulled \(name)", "drive")
                }
            }
            return found
        }

        outcome.lessons = pull("lessons", ext: "rolesson") + pull("", ext: "rolesson")
        outcome.notes = pull("notes", ext: "roanalysis") + pull("", ext: "roanalysis")

        // The diagnostic log goes up too, so it can be read on the computer
        // without anyone copying it off the phone.
        if let log {
            let logsDir = root.appendingPathComponent("logs", isDirectory: true)
            var logError: NSError?
            coordinator.coordinate(writingItemAt: logsDir.appendingPathComponent("vorbeste-log.txt"),
                                   options: [.forReplacing], error: &logError) { url in
                try? fm.createDirectory(at: logsDir, withIntermediateDirectories: true)
                try? log.write(to: url)
            }
        }

        guard !outgoing.isEmpty else { return outcome }
        for folder in Set(outgoing.map(\.folder)) {
            var dirError: NSError?
            coordinator.coordinate(writingItemAt: root.appendingPathComponent(folder, isDirectory: true),
                                   options: [], error: &dirError) { url in
                try? fm.createDirectory(at: url, withIntermediateDirectories: true)
            }
        }
        for o in outgoing {
            let target = root.appendingPathComponent(o.folder, isDirectory: true).appendingPathComponent(o.fileName)
            var ok = false
            var writeError: NSError?
            coordinator.coordinate(writingItemAt: target, options: [.forReplacing], error: &writeError) { url in
                ok = (try? o.data.write(to: url)) != nil
            }
            if ok {
                outcome.pushed.append(o.key)
                Log.write("wrote \(o.folder)/\(o.fileName)", "drive")
            } else {
                outcome.problem = writeError?.localizedDescription ?? "Couldn't write \(o.fileName)"
                Log.write("write \(o.folder)/\(o.fileName) failed: \(writeError.map { "\($0.domain) \($0.code) \($0.localizedDescription)" } ?? "no error given")", "drive")
            }
        }
        return outcome
    }
}
