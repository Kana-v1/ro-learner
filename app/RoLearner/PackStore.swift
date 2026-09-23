import Foundation

struct Pack: Identifiable {
    let header: PackHeader
    let audioURL: URL
    var id: String { header.slug }
}

enum PackError: LocalizedError {
    case notALesson, damaged
    var errorDescription: String? {
        switch self {
        case .notALesson: return "Not a .rolesson file."
        case .damaged: return "The lesson file is damaged or incomplete."
        }
    }
}

/// Episodes and results on disk. Documents/ is visible in the Files app
/// (UIFileSharingEnabled), so lessons can be dropped in and results picked up
/// there as well as through the import button and share sheet.
@MainActor
final class PackStore: ObservableObject {
    @Published private(set) var packs: [Pack] = []
    @Published private(set) var sessions: [SessionRecord] = []   // newest first
    @Published var lastError: String?

    /// File layout, matching make_lesson_pack.py: magic, 4-byte big-endian
    /// header length, JSON header, then the mp3 bytes to the end of the file.
    static let magic = Data("ROLESSON1\n".utf8)

    let docs = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    var packsDir: URL { docs.appendingPathComponent("Packs", isDirectory: true) }
    var resultsDir: URL { docs.appendingPathComponent("Results", isDirectory: true) }

    init() {
        let fm = FileManager.default
        try? fm.createDirectory(at: packsDir, withIntermediateDirectories: true)
        try? fm.createDirectory(at: resultsDir, withIntermediateDirectories: true)
        importDropped()
        reload()
    }

    /// Lesson files dropped into the app's folder through the Files app.
    func importDropped() {
        let fm = FileManager.default
        let places = [docs, docs.appendingPathComponent("Inbox")]
        for place in places {
            let files = (try? fm.contentsOfDirectory(at: place, includingPropertiesForKeys: nil)) ?? []
            for url in files where url.pathExtension == "rolesson" {
                do {
                    try importPack(from: url)
                    try? fm.removeItem(at: url)
                } catch {
                    lastError = "\(url.lastPathComponent): \(error.localizedDescription)"
                }
            }
        }
    }

    /// Files chosen in the document picker (Google Drive, iCloud, On My iPhone).
    func importPicked(_ urls: [URL]) {
        for url in urls {
            let scoped = url.startAccessingSecurityScopedResource()
            defer { if scoped { url.stopAccessingSecurityScopedResource() } }
            do { try importPack(from: url) } catch {
                lastError = "\(url.lastPathComponent): \(error.localizedDescription)"
            }
        }
        reload()
    }

    private func importPack(from url: URL) throws {
        let data = try Data(contentsOf: url)
        guard data.starts(with: Self.magic) else { throw PackError.notALesson }
        var p = Self.magic.count
        guard data.count >= p + 4 else { throw PackError.damaged }
        let len = data[p..<p + 4].reduce(0) { ($0 << 8) | Int($1) }
        p += 4
        guard data.count > p + len else { throw PackError.damaged }
        let headerData = Data(data[p..<p + len])
        let header = try JSONDecoder().decode(PackHeader.self, from: headerData)
        let audio = Data(data[(p + len)...])

        let dir = packsDir.appendingPathComponent(header.slug, isDirectory: true)
        try? FileManager.default.removeItem(at: dir)
        try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        try headerData.write(to: dir.appendingPathComponent("header.json"))
        try audio.write(to: dir.appendingPathComponent("audio.mp3"))
    }

    func reload() {
        let fm = FileManager.default
        let dirs = (try? fm.contentsOfDirectory(at: packsDir, includingPropertiesForKeys: nil)) ?? []
        packs = dirs.compactMap { dir -> Pack? in
            guard let d = try? Data(contentsOf: dir.appendingPathComponent("header.json")),
                  let h = try? JSONDecoder().decode(PackHeader.self, from: d) else { return nil }
            return Pack(header: h, audioURL: dir.appendingPathComponent("audio.mp3"))
        }
        .sorted { $0.header.slug < $1.header.slug }

        let dec = JSONDecoder()
        dec.dateDecodingStrategy = .iso8601
        let files = (try? fm.contentsOfDirectory(at: resultsDir, includingPropertiesForKeys: nil)) ?? []
        sessions = files.filter { $0.pathExtension == "json" }
            .compactMap { try? dec.decode(SessionRecord.self, from: Data(contentsOf: $0)) }
            .sorted { $0.started > $1.started }
    }

    func delete(_ pack: Pack) {
        try? FileManager.default.removeItem(at: pack.audioURL.deletingLastPathComponent())
        reload()
    }

    private static var encoder: JSONEncoder {
        let enc = JSONEncoder()
        enc.dateEncodingStrategy = .iso8601
        enc.outputFormatting = [.prettyPrinted, .sortedKeys]
        return enc
    }

    func save(_ s: SessionRecord) {
        let name = "\(s.episode)_\(Int(s.started.timeIntervalSince1970)).json"
        if let d = try? Self.encoder.encode(s) {
            try? d.write(to: resultsDir.appendingPathComponent(name), options: .atomic)
        }
    }

    /// Every session in one file, for the share sheet ("Save to Files" -> Drive).
    func exportAll() -> URL? {
        reload()
        guard !sessions.isEmpty, let d = try? Self.encoder.encode(sessions) else { return nil }
        let f = DateFormatter()
        f.dateFormat = "yyyy-MM-dd_HHmm"
        let url = FileManager.default.temporaryDirectory
            .appendingPathComponent("ro-results_\(f.string(from: Date())).json")
        try? d.write(to: url, options: .atomic)
        return url
    }

    /// "7/12" for the most recent listen of an episode, first-pass answers only.
    func lastScore(for slug: String) -> String? {
        guard let s = sessions.first(where: { $0.episode == slug }) else { return nil }
        let main = s.items.filter { !$0.retry && $0.verdict != .unmarked }
        guard !main.isEmpty else { return nil }
        return "\(main.filter { $0.verdict == .correct }.count)/\(main.count)"
    }
}
