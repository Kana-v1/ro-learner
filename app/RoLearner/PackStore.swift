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

/// What the home screen tells the learner to do next. The loop is
/// import → practise → upload results → ask Claude, and back round.
enum NextStep {
    case importEpisodes
    case continueEpisode(Pack, SavedProgress)
    case practise(Pack)
    case upload(Int)
    case askClaude(Int)
    case allDone

    /// Which of the four loop stages this belongs to (0-based).
    var stage: Int {
        switch self {
        case .importEpisodes: return 0
        case .continueEpisode, .practise, .allDone: return 1
        case .upload: return 2
        case .askClaude: return 3
        }
    }
}

/// Episodes, results and progress on disk.
///
/// Documents/ is visible in the Files app (UIFileSharingEnabled): lessons can be
/// dropped in there and results picked up. Resume points and upload status are
/// internal and live in Application Support instead.
@MainActor
final class PackStore: ObservableObject {
    @Published private(set) var packs: [Pack] = []
    @Published private(set) var sessions: [SessionRecord] = []          // newest first
    @Published private(set) var progress: [String: SavedProgress] = [:]  // by episode slug
    @Published private(set) var status = AnalysisStatus()
    @Published private(set) var notes: [AnalysisNote] = []              // newest first
    @Published private(set) var linkedFolder: String?                   // display name of the Drive folder
    @Published private(set) var syncing = false
    @Published private(set) var lastSync: Date?
    @Published private(set) var syncProblem: String?
    @Published private(set) var githubRepo: String? = UserDefaults.standard.string(forKey: "githubRepo")
    @Published var lastError: String?

    /// File layout, matching make_lesson_pack.py: magic, 4-byte big-endian
    /// header length, JSON header, then the mp3 bytes to the end of the file.
    static let magic = Data("ROLESSON1\n".utf8)

    private let fm = FileManager.default
    let docs = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    private let support = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
    var packsDir: URL { docs.appendingPathComponent("Packs", isDirectory: true) }
    var resultsDir: URL { docs.appendingPathComponent("Results", isDirectory: true) }
    var reportsDir: URL { docs.appendingPathComponent("Claude notes", isDirectory: true) }
    var feedbackDir: URL { docs.appendingPathComponent("Feedback", isDirectory: true) }
    private var progressDir: URL { support.appendingPathComponent("Progress", isDirectory: true) }
    private var statusURL: URL { support.appendingPathComponent("status.json") }
    private var bookmarkURL: URL { support.appendingPathComponent("drive-folder.bookmark") }

    static var encoder: JSONEncoder {
        let enc = JSONEncoder()
        enc.dateEncodingStrategy = .iso8601
        enc.outputFormatting = [.prettyPrinted, .sortedKeys]
        return enc
    }

    static var decoder: JSONDecoder {
        let dec = JSONDecoder()
        dec.dateDecodingStrategy = .iso8601
        return dec
    }

    init() {
        for d in [packsDir, resultsDir, reportsDir, progressDir, feedbackDir] {
            try? fm.createDirectory(at: d, withIntermediateDirectories: true)
        }
        if let d = try? Data(contentsOf: statusURL),
           let s = try? Self.decoder.decode(AnalysisStatus.self, from: d) {
            status = s
        }
        linkedFolder = resolveLinkedFolder()?.lastPathComponent
        importDropped()
        reload()
    }

    // MARK: the linked Drive folder

    /// Remember a folder picked in the document picker. The bookmark keeps the
    /// app's access to it across launches.
    func linkFolder(_ url: URL) {
        let scoped = url.startAccessingSecurityScopedResource()
        defer { if scoped { url.stopAccessingSecurityScopedResource() } }
        Log.write("link folder \(url.path) (scoped access: \(scoped))", "drive")
        do {
            // Apple's own sample for folders picked in the Files app keeps a
            // minimal bookmark; that is what survives relaunches for them.
            let data = try url.bookmarkData(options: .minimalBookmark, includingResourceValuesForKeys: nil, relativeTo: nil)
            try data.write(to: bookmarkURL, options: .atomic)
            linkedFolder = url.lastPathComponent
            syncProblem = nil
            Log.write("linked: bookmark \(data.count) bytes", "drive")
        } catch {
            Log.write("link failed: \(error)", "drive")
            lastError = "Couldn't link that folder: \(error.localizedDescription)"
        }
    }

    func unlinkFolder() {
        try? fm.removeItem(at: bookmarkURL)
        linkedFolder = nil
        syncProblem = nil
    }

    private func resolveLinkedFolder() -> URL? {
        guard let data = try? Data(contentsOf: bookmarkURL) else { return nil }
        var stale = false
        let url: URL
        do {
            url = try URL(resolvingBookmarkData: data, options: [], relativeTo: nil, bookmarkDataIsStale: &stale)
        } catch {
            Log.write("can't open the linked folder's bookmark: \(error)", "drive")
            return nil
        }
        if stale, url.startAccessingSecurityScopedResource() {
            Log.write("bookmark was stale; refreshing", "drive")
            if let fresh = try? url.bookmarkData(options: .minimalBookmark, includingResourceValuesForKeys: nil, relativeTo: nil) {
                try? fresh.write(to: bookmarkURL, options: .atomic)
            }
            url.stopAccessingSecurityScopedResource()
        }
        return url
    }

    /// Pull new lessons and Claude's notes from the linked folder, push finished
    /// sessions into its results/ folder. Safe to call often; does nothing
    /// without a linked folder.
    // MARK: GitHub sync (preferred over the iCloud folder when set up)

    var githubConfigured: Bool { githubRepo != nil && Keychain.get("githubToken") != nil }
    /// Episodes arrive and results leave by themselves (GitHub or iCloud).
    var autoSync: Bool { githubConfigured || linkedFolder != nil }

    /// Check the token against the repo, keep it in the Keychain, sync.
    /// Returns a message to show when GitHub refuses.
    func connectGitHub(repo rawRepo: String, token rawToken: String) async -> String? {
        let repo = rawRepo.trimmingCharacters(in: .whitespacesAndNewlines)
        let token = rawToken.trimmingCharacters(in: .whitespacesAndNewlines)
        guard repo.contains("/"), !token.isEmpty else { return "Enter owner/repo and the token." }
        if let problem = await GitHubSync.check(repo: repo, token: token) { return problem }
        Keychain.set(token, for: "githubToken")
        UserDefaults.standard.set(repo, forKey: "githubRepo")
        githubRepo = repo
        // Results "sent" to iCloud never reached the computer: send everything once more.
        status.sent = [:]
        saveStatus()
        Log.write("connected to GitHub repo \(repo)", "sync")
        await sync()
        return nil
    }

    func disconnectGitHub() {
        Keychain.set(nil, for: "githubToken")
        UserDefaults.standard.removeObject(forKey: "githubRepo")
        githubRepo = nil
        syncProblem = nil
    }

    func sync() async {
        guard !syncing else { return }
        let gitHub = githubRepo.flatMap { repo in Keychain.get("githubToken").map { (repo: repo, token: $0) } }
        let root = gitHub == nil ? resolveLinkedFolder() : nil
        guard gitHub != nil || root != nil else { return }
        syncing = true
        defer { syncing = false }

        var outgoing = unsent.compactMap { s -> DriveSync.Outgoing? in
            guard let d = try? Self.encoder.encode(s) else { return nil }
            return DriveSync.Outgoing(key: s.key, fileName: "\(s.key).json", data: d)
        }
        outgoing += unsentFeedback.compactMap { url -> DriveSync.Outgoing? in
            guard let d = try? Data(contentsOf: url) else { return nil }
            let name = url.lastPathComponent
            return DriveSync.Outgoing(key: "fb:\(name)", fileName: name, data: d, folder: "feedback")
        }
        let known = status.pulled
        let logData = Data(Log.read().utf8)
        let outcome: DriveSync.Outcome
        if let gitHub {
            let result = await GitHubSync.run(repo: gitHub.repo, token: gitHub.token, known: known,
                                              haveSlugs: Set(packs.map(\.header.slug)),
                                              outgoing: outgoing, log: logData)
            for (k, d) in result.1 { status.pulled[k] = d }
            outcome = result.0
        } else if let root {
            outcome = await Task.detached(priority: .utility) {
                DriveSync.run(root: root, known: known, outgoing: outgoing, log: logData)
            }.value
        } else {
            return
        }

        for f in outcome.lessons {
            do { try importPack(from: f.local); status.pulled[f.name] = f.modified }
            catch {
                Log.write("import \(f.name) failed: \(error)", "drive")
                lastError = "\(f.name): \(error.localizedDescription)"
            }
        }
        for f in outcome.notes {
            do { try importNote(from: f.local); status.pulled[f.name] = f.modified }
            catch { lastError = "\(f.name): \(error.localizedDescription)" }
        }
        let now = Date()
        for k in outcome.pushed { status.sent[k] = now }
        saveStatus()
        syncProblem = outcome.problem
        Log.write("sync done: \(outcome.lessons.count) lesson(s), \(outcome.notes.count) note(s) in, \(outcome.pushed.count)/\(outgoing.count) result(s) out\(outcome.problem.map { "; problem: \($0)" } ?? "")", "drive")
        lastSync = now
        reload()
    }

    // MARK: feedback

    /// Feedback notes not uploaded yet.
    var unsentFeedback: [URL] {
        jsonFiles(in: feedbackDir).filter { status.sent["fb:\($0.lastPathComponent)"] == nil }
    }

    /// Keep a note and send it straight away when sync is set up.
    func addFeedback(_ note: FeedbackNote) {
        let url = feedbackDir.appendingPathComponent("\(note.id).json")
        do {
            try Self.encoder.encode(note).write(to: url, options: .atomic)
            Log.write("feedback saved: \(note.kind) \(note.episode ?? "-") \(note.drill ?? "")", "ui")
        } catch {
            lastError = "Couldn't save the feedback: \(error.localizedDescription)"
            return
        }
        if autoSync { Task { await sync() } }
    }

    // MARK: importing

    /// Lesson and note files dropped into the app's folder through the Files app.
    func importDropped() {
        for place in [docs, docs.appendingPathComponent("Inbox")] {
            let files = (try? fm.contentsOfDirectory(at: place, includingPropertiesForKeys: nil)) ?? []
            for url in files where ["rolesson", "roanalysis"].contains(url.pathExtension) {
                do {
                    try importFile(url)
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
            do { try importFile(url) } catch {
                lastError = "\(url.lastPathComponent): \(error.localizedDescription)"
            }
        }
        reload()
    }

    private func importFile(_ url: URL) throws {
        if url.pathExtension == "roanalysis" { try importNote(from: url) } else { try importPack(from: url) }
    }

    private func importNote(from url: URL) throws {
        let data = try Data(contentsOf: url)
        let note = try Self.decoder.decode(AnalysisNote.self, from: data)
        let name = "note_\(Int(note.created.timeIntervalSince1970)).json"
        try data.write(to: reportsDir.appendingPathComponent(name), options: .atomic)
        status.analyzed.formUnion(note.analyzed)
        saveStatus()
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
        try? fm.removeItem(at: dir)
        try fm.createDirectory(at: dir, withIntermediateDirectories: true)
        try headerData.write(to: dir.appendingPathComponent("header.json"))
        try audio.write(to: dir.appendingPathComponent("audio.mp3"))
    }

    // MARK: loading

    func reload() {
        let dirs = (try? fm.contentsOfDirectory(at: packsDir, includingPropertiesForKeys: nil)) ?? []
        packs = dirs.compactMap { dir -> Pack? in
            guard let d = try? Data(contentsOf: dir.appendingPathComponent("header.json")),
                  let h = try? JSONDecoder().decode(PackHeader.self, from: d) else { return nil }
            return Pack(header: h, audioURL: dir.appendingPathComponent("audio.mp3"))
        }
        .sorted { $0.header.slug < $1.header.slug }

        sessions = jsonFiles(in: resultsDir)
            .compactMap { try? Self.decoder.decode(SessionRecord.self, from: Data(contentsOf: $0)) }
            .sorted { $0.started > $1.started }

        notes = jsonFiles(in: reportsDir)
            .compactMap { try? Self.decoder.decode(AnalysisNote.self, from: Data(contentsOf: $0)) }
            .sorted { $0.created > $1.created }

        var loaded: [String: SavedProgress] = [:]
        for url in jsonFiles(in: progressDir) {
            if let p = try? Self.decoder.decode(SavedProgress.self, from: Data(contentsOf: url)) {
                loaded[p.record.episode] = p
            }
        }
        progress = loaded
    }

    private func jsonFiles(in dir: URL) -> [URL] {
        ((try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil)) ?? [])
            .filter { $0.pathExtension == "json" }
    }

    func delete(_ pack: Pack) {
        try? fm.removeItem(at: pack.audioURL.deletingLastPathComponent())
        clearProgress(pack.header.slug)
        reload()
    }

    // MARK: sessions and progress

    func save(_ s: SessionRecord) {
        let url = resultsDir.appendingPathComponent("\(s.key).json")
        if let d = try? Self.encoder.encode(s) { try? d.write(to: url, options: .atomic) }
        if let i = sessions.firstIndex(where: { $0.key == s.key }) { sessions[i] = s }
        else { sessions.insert(s, at: 0) }
    }

    func saveProgress(_ p: SavedProgress) {
        let url = progressDir.appendingPathComponent("\(p.record.episode).json")
        if let d = try? Self.encoder.encode(p) { try? d.write(to: url, options: .atomic) }
        progress[p.record.episode] = p
    }

    func clearProgress(_ slug: String) {
        try? fm.removeItem(at: progressDir.appendingPathComponent("\(slug).json"))
        progress[slug] = nil
    }

    /// "Start over": the answers given so far still count as a session.
    func startOver(_ slug: String) {
        if var p = progress[slug], !p.record.items.isEmpty {
            p.record.finished = Date()
            save(p.record)
        }
        clearProgress(slug)
    }

    // MARK: the road to Claude

    /// Practice finished but not uploaded yet.
    var unsent: [SessionRecord] {
        sessions.filter { $0.finished != nil && !$0.items.isEmpty
            && status.sent[$0.key] == nil && !status.analyzed.contains($0.key) }
    }

    /// Uploaded, and Claude has not been asked (or has not answered) yet.
    var awaiting: [SessionRecord] {
        sessions.filter { status.sent[$0.key] != nil && !status.analyzed.contains($0.key) }
    }

    enum Stage { case inProgress, notSent, sent, analyzed }

    func stage(of s: SessionRecord) -> Stage {
        if status.analyzed.contains(s.key) { return .analyzed }
        if status.sent[s.key] != nil { return .sent }
        return s.finished == nil ? .inProgress : .notSent
    }

    /// One file holding every session not yet uploaded, for the share sheet.
    func exportUnsent() -> ShareItem? {
        let batch = unsent
        guard !batch.isEmpty else { return nil }
        struct Export: Codable {
            let format: Int
            let exported: Date
            let sessions: [SessionRecord]
        }
        guard let d = try? Self.encoder.encode(Export(format: 2, exported: Date(), sessions: batch)) else { return nil }
        let f = DateFormatter()
        f.dateFormat = "yyyy-MM-dd_HHmm"
        let url = fm.temporaryDirectory.appendingPathComponent("vorbeste-results_\(f.string(from: Date())).json")
        do { try d.write(to: url, options: .atomic) } catch { return nil }
        return ShareItem(url: url, keys: batch.map(\.key))
    }

    func markSent(_ keys: [String]) {
        let now = Date()
        for k in keys where status.sent[k] == nil { status.sent[k] = now }
        saveStatus()
    }

    /// "I've asked Claude": closes the loop without waiting for a note file.
    func markAnalysed(_ keys: [String]) {
        status.analyzed.formUnion(keys)
        saveStatus()
    }

    private func saveStatus() {
        if let d = try? Self.encoder.encode(status) { try? d.write(to: statusURL, options: .atomic) }
        objectWillChange.send()
    }

    // MARK: guidance

    var inProgress: [(pack: Pack, progress: SavedProgress)] {
        packs.compactMap { p in progress[p.header.slug].map { (pack: p, progress: $0) } }
            .sorted { $0.progress.savedAt > $1.progress.savedAt }
    }

    var nextStep: NextStep {
        if packs.isEmpty { return .importEpisodes }
        if !unsent.isEmpty { return .upload(unsent.count) }
        if !awaiting.isEmpty { return .askClaude(awaiting.count) }
        if let first = inProgress.first { return .continueEpisode(first.pack, first.progress) }
        if let fresh = packs.first(where: isNew) { return .practise(fresh) }
        return .allDone
    }

    // MARK: episode status, for filtering and sorting a long list

    enum EpisodeState: String, CaseIterable {
        case new = "New", inProgress = "In progress", done = "Done"
    }

    /// The latest finished session of each episode (sessions are newest first).
    func lastFinished(_ slug: String) -> SessionRecord? {
        sessions.first { $0.episode == slug && $0.finished != nil }
    }

    /// Share of drills right first time in the latest finished session, over all
    /// the episode's drills, so skipping most of an episode doesn't count as done.
    func lastScore(_ pack: Pack) -> Double? {
        guard let s = lastFinished(pack.header.slug) else { return nil }
        let total = max(pack.header.drills.count, 1)
        if s.mode == "voice" { return Double(s.rightFirstTime) / Double(total) }
        let heard = s.mainItems.count
        let wrong = s.mainItems.filter { $0.outcome == .missed }.count
        return Double(heard - wrong) / Double(total)
    }

    /// Finished is done, whatever the score: episodes are not replayed to
    /// polish a number — what was missed comes back in later episodes' reviews.
    /// The score stays visible in the row's subtitle.
    func state(of pack: Pack) -> EpisodeState {
        let slug = pack.header.slug
        if progress[slug] != nil { return .inProgress }
        return lastFinished(slug) != nil ? .done : .new
    }

    /// When the episode was last listened to (finished or not).
    func lastPlayed(_ pack: Pack) -> Date? {
        let slug = pack.header.slug
        let session = sessions.first { $0.episode == slug }?.started
        let saved = progress[slug]?.savedAt
        return [session, saved].compactMap { $0 }.max()
    }

    func isNew(_ pack: Pack) -> Bool {
        let slug = pack.header.slug
        return progress[slug] == nil && !sessions.contains { $0.episode == slug }
    }

    func subtitle(for pack: Pack) -> String {
        let slug = pack.header.slug
        let total = pack.header.drills.count
        if let p = progress[slug] {
            let done = p.record.mainItems.count
            return "In progress · drill \(min(done + 1, total)) of \(total)"
        }
        if let s = sessions.first(where: { $0.episode == slug && $0.finished != nil }) {
            if s.mode == "voice" { return "Last time: \(s.rightFirstTime) of \(s.mainItems.count) right" }
            let wrong = s.mainItems.filter { $0.outcome == .missed }.count
            return "Practised · \(wrong) marked wrong"
        }
        return "\(total) drills · \(Int((pack.header.duration / 60).rounded())) min"
    }
}
