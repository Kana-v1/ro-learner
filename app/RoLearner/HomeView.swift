import SwiftUI
import UniformTypeIdentifiers

/// An episode about to open in the player, with where to pick up (if anywhere).
struct PlayerLaunch: Identifiable {
    let pack: Pack
    let resume: SavedProgress?
    var id: String { pack.id }
}

struct HomeView: View {
    @EnvironmentObject private var store: PackStore
    @AppStorage("voiceMode") private var voiceMode = true
    // Off by default: in call mode the AirPods mic missed answers and presses
    // were unreliable. Kept as an experiment (voice-chat mode) until it works.
    @AppStorage("headsetMicExperimental") private var headsetMic = false
    @AppStorage("serverRecognition") private var serverRecognition = true
    @AppStorage("onboarded") private var onboarded = false
    @State private var importing = false
    @State private var linking = false
    @State private var launch: PlayerLaunch?
    @State private var resumeCandidate: Pack?
    @State private var pendingLaunch: PlayerLaunch?
    @State private var share: ShareItem?
    @State private var showResults = false
    @State private var filter: EpisodeFilter = .all
    @State private var sort: EpisodeSort = .course
    @State private var query = ""
    @State private var flipped: Set<Int> = []    // lessons opened/closed against their default

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                header
                NextStepCard(step: store.nextStep, linked: store.linkedFolder != nil,
                             syncing: store.syncing, act: act)
                if let first = store.inProgress.first, !isContinueStep {
                    ContinueCard(pack: first.pack, progress: first.progress) { open(first.pack) }
                }
                episodes
                settings
            }
            .padding(.horizontal, 20)
            .padding(.top, 12)
            .padding(.bottom, 32)
        }
        .refreshable { await store.sync() }
        .shakeForLog()
        .background(Theme.bg.ignoresSafeArea())
        .foregroundStyle(Theme.text)
        .fileImporter(isPresented: $importing, allowedContentTypes: [.item],
                      allowsMultipleSelection: true) { result in
            switch result {
            case .success(let urls):
                Log.write("import picked \(urls.count) file(s)", "ui")
                store.importPicked(urls)
            case .failure(let error):
                Log.write("import picker failed: \(error)", "ui")
            }
        }
        // A sheet rather than a full-screen cover, so it can be swiped down;
        // swiping closes the player exactly like its X (PlayerView.onDisappear).
        .sheet(item: $launch) { l in
            PlayerView(launch: l, store: store, voiceMode: voiceMode, headsetMic: headsetMic)
                .environmentObject(store)
                .presentationDragIndicator(.visible)
                .presentationBackground(Theme.bg)
        }
        .sheet(item: $resumeCandidate, onDismiss: {
            launch = pendingLaunch
            pendingLaunch = nil
        }) { pack in
            ResumeSheet(pack: pack, progress: store.progress[pack.header.slug],
                        onContinue: {
                            pendingLaunch = PlayerLaunch(pack: pack, resume: store.progress[pack.header.slug])
                            resumeCandidate = nil
                        },
                        onStartOver: {
                            store.startOver(pack.header.slug)
                            pendingLaunch = PlayerLaunch(pack: pack, resume: nil)
                            resumeCandidate = nil
                        })
                .presentationDetents([.height(440)])
                .presentationBackground(Theme.raised)
        }
        .sheet(item: $share) { item in
            ShareSheet(items: [item.url]) { done in
                if done { store.markSent(item.keys) }
                share = nil
            }
            .presentationDetents([.medium, .large])
        }
        .sheet(isPresented: $showResults) {
            ResultsView().environmentObject(store)
        }
        .fullScreenCover(isPresented: Binding(get: { !onboarded }, set: { onboarded = !$0 })) {
            OnboardingView { onboarded = true }.environmentObject(store)
        }
        .alert("Import problem", isPresented: Binding(
            get: { store.lastError != nil },
            set: { if !$0 { store.lastError = nil } }
        )) {
            Button("OK") {}
        } message: {
            Text(store.lastError ?? "")
        }
    }

    private var isContinueStep: Bool {
        if case .continueEpisode = store.nextStep { return true }
        return false
    }

    private var header: some View {
        HStack {
            Text("Vorbește").font(Theme.display(32))
            Spacer()
            CircleIconButton(symbol: "chart.bar", label: "Results") { showResults = true }
        }
    }

    // MARK: episodes — grouped, filtered, searchable, for a course of ~200 parts

    private var visiblePacks: [Pack] {
        let q = query.trimmingCharacters(in: .whitespaces).lowercased()
        let list = store.packs.filter { pack in
            (filter.state.map { store.state(of: pack) == $0 } ?? true)
                && (q.isEmpty || pack.header.title.lowercased().contains(q)
                    || pack.header.slug.lowercased().contains(q))
        }
        switch sort {
        case .course:
            return list
        case .recent:
            return list.sorted { (store.lastPlayed($0) ?? .distantPast) > (store.lastPlayed($1) ?? .distantPast) }
        case .weakest:
            // practised episodes, lowest score first; never-played ones after
            return list.sorted { (store.lastScore($0) ?? 2) < (store.lastScore($1) ?? 2) }
        }
    }

    private var episodes: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Episodes").font(.system(size: 17, weight: .semibold))
                Text("\(store.packs.count)").font(.system(size: 15)).foregroundStyle(Theme.muted)
                Spacer()
                Menu {
                    Picker("Sort", selection: $sort) {
                        ForEach(EpisodeSort.allCases) { Text($0.rawValue).tag($0) }
                    }
                } label: {
                    Image(systemName: "arrow.up.arrow.down").font(.system(size: 15, weight: .medium))
                        .frame(width: 36, height: 36).overlay(Circle().stroke(Theme.line))
                }
                .foregroundStyle(Theme.text)
                .accessibilityLabel("Sort episodes")
                Button { importing = true } label: {
                    Label("Import", systemImage: "plus").font(.system(size: 14, weight: .medium))
                        .padding(.horizontal, 12).frame(height: 36)
                        .overlay(Capsule().stroke(Theme.line))
                }
                .foregroundStyle(Theme.text)
            }
            if store.packs.count > 6 {
                HStack(spacing: 8) {
                    Image(systemName: "magnifyingglass").foregroundStyle(Theme.muted)
                    TextField("Search episodes", text: $query)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                    if !query.isEmpty {
                        Button { query = "" } label: { Image(systemName: "xmark.circle.fill") }
                            .foregroundStyle(Theme.muted)
                            .accessibilityLabel("Clear search")
                    }
                }
                .padding(.horizontal, 12).frame(height: 40)
                .background(Theme.surface, in: RoundedRectangle(cornerRadius: 12))
                .overlay(RoundedRectangle(cornerRadius: 12).stroke(Theme.line))
            }
            if !store.packs.isEmpty {
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(EpisodeFilter.allCases) { f in
                            let count = f.state.map { st in store.packs.filter { store.state(of: $0) == st }.count }
                                ?? store.packs.count
                            Button { filter = f } label: {
                                Text("\(f.rawValue) \(count)")
                                    .font(.system(size: 13, weight: .semibold))
                                    .padding(.horizontal, 12).frame(height: 32)
                                    .foregroundStyle(filter == f ? Theme.onAccent : Theme.text2)
                                    .background(filter == f ? Theme.accent : Theme.surface, in: Capsule())
                                    .overlay(Capsule().stroke(filter == f ? Color.clear : Theme.line))
                            }
                        }
                    }
                }
            }
            if store.packs.isEmpty {
                Text("No episodes yet.").foregroundStyle(Theme.muted)
            } else if visiblePacks.isEmpty {
                Text("Nothing matches.").foregroundStyle(Theme.muted)
            } else if sort == .course {
                ForEach(lessons, id: \.self) { lesson in
                    lessonGroup(lesson)
                }
            } else {
                episodeList(visiblePacks)
            }
        }
    }

    private var lessons: [Int] {
        Array(Set(visiblePacks.map(\.header.lesson))).sorted()
    }

    /// A lesson is folded when every part of it is done, unless the user
    /// opened it; while filtering or searching everything is shown open.
    private func isOpen(_ lesson: Int) -> Bool {
        if filter != .all || !query.isEmpty { return true }
        let parts = store.packs.filter { $0.header.lesson == lesson }
        let allDone = !parts.isEmpty && parts.allSatisfy { store.state(of: $0) == .done }
        return allDone == flipped.contains(lesson)
    }

    private func lessonGroup(_ lesson: Int) -> some View {
        let parts = visiblePacks.filter { $0.header.lesson == lesson }
        let all = store.packs.filter { $0.header.lesson == lesson }
        let done = all.filter { store.state(of: $0) == .done }.count
        let open = isOpen(lesson)
        return VStack(alignment: .leading, spacing: 8) {
            Button {
                if flipped.contains(lesson) { flipped.remove(lesson) } else { flipped.insert(lesson) }
            } label: {
                HStack {
                    Text(lesson == 0 ? "Other" : "Lesson \(lesson)").font(.system(size: 15, weight: .semibold))
                    Text("\(done)/\(all.count) done").font(.system(size: 13)).foregroundStyle(Theme.muted)
                    Spacer()
                    Image(systemName: open ? "chevron.up" : "chevron.down")
                        .font(.system(size: 13, weight: .semibold)).foregroundStyle(Theme.muted)
                }
                .frame(minHeight: 36)
                .contentShape(Rectangle())
            }
            .buttonStyle(.plain)
            .foregroundStyle(Theme.text)
            .accessibilityLabel("Lesson \(lesson), \(done) of \(all.count) done, \(open ? "open" : "closed")")
            if open { episodeList(parts) }
        }
    }

    private func episodeList(_ packs: [Pack]) -> some View {
        VStack(spacing: 0) {
            ForEach(Array(packs.enumerated()), id: \.element.id) { k, pack in
                EpisodeRow(pack: pack, subtitle: store.subtitle(for: pack), state: store.state(of: pack)) {
                    open(pack)
                }
                .overlay(alignment: .top) {
                    if k > 0 { Rectangle().fill(Color(hex: 0x232934)).frame(height: 1) }
                }
                .contextMenu {
                    Button(role: .destructive) { store.delete(pack) } label: {
                        Label("Remove episode", systemImage: "trash")
                    }
                }
            }
        }
        .background(Theme.surface, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 18, style: .continuous).stroke(Theme.line))
    }

    private var settings: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Settings").font(.system(size: 17, weight: .semibold)).padding(.top, 8)
            CardBox {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text("Sync folder").font(.system(size: 15, weight: .semibold))
                            Text(driveStatus).font(.system(size: 13)).foregroundStyle(Theme.muted)
                        }
                        Spacer()
                        if store.syncing { ProgressView().tint(Theme.accent) }
                    }
                    if store.linkedFolder == nil {
                        Button("Link iCloud Drive folder") {
                            Log.write("tapped Link Drive folder", "ui")
                            linking = true
                        }
                        .buttonStyle(OutlineButtonStyle())
                    } else {
                        HStack(spacing: 10) {
                            Button("Sync now") {
                                Log.write("tapped Sync now", "ui")
                                Task { await store.sync() }
                            }
                            .buttonStyle(OutlineButtonStyle())
                            Button("Unlink") { store.unlinkFolder() }.buttonStyle(OutlineButtonStyle())
                        }
                    }
                    Text("A folder in iCloud Drive (Google Drive doesn't let other apps open its folders). Whenever the app is open, new episodes come in from its lessons/ and your results go out to results/, where Claude reads them.")
                        .font(.system(size: 12)).foregroundStyle(Theme.muted)
                }
                Divider().overlay(Theme.line)
                Toggle("Listen to my answers", isOn: $voiceMode).tint(Theme.accent)
                Toggle("Better recognition (Apple's servers)", isOn: $serverRecognition).tint(Theme.accent)
                Text("Sends your spoken answers to Apple to be recognised, which is more accurate for Romanian. Needs a connection; without one the phone recognises them itself.")
                    .font(.system(size: 12)).foregroundStyle(Theme.muted)
                Toggle("Headphone microphone (experimental)", isOn: $headsetMic).tint(Theme.accent)
                Text("With listening off, episodes play straight through and you mark misses yourself. The headphone microphone runs the app like a phone call: call-quality sound, noise suppression, and AirPods presses as pause/resume. Still being tested; off, the phone's microphone listens and playback stays full quality.")
                    .font(.system(size: 12)).foregroundStyle(Theme.muted)
            }
        }
        .linkFolderPicker(isPresented: $linking, store: store)
    }

    private var driveStatus: String {
        guard let name = store.linkedFolder else { return "Not linked" }
        if let p = store.syncProblem { return "\(name) · \(p)" }
        if let t = store.lastSync { return "\(name) · synced \(t.formatted(date: .omitted, time: .shortened))" }
        return name
    }

    private func act(_ step: NextStep) {
        switch step {
        case .importEpisodes, .allDone:
            if store.linkedFolder != nil { Task { await store.sync() } } else { importing = true }
        case .upload:
            if store.linkedFolder != nil { Task { await store.sync() } } else { share = store.exportUnsent() }
        case .askClaude:
            store.markAnalysed(store.awaiting.map(\.key))
        case .continueEpisode(let pack, _), .practise(let pack):
            open(pack)
        }
    }

    private func open(_ pack: Pack) {
        if store.progress[pack.header.slug] != nil {
            resumeCandidate = pack
        } else {
            launch = PlayerLaunch(pack: pack, resume: nil)
        }
    }
}

// MARK: - pieces

struct NextStepCard: View {
    let step: NextStep
    let linked: Bool
    let syncing: Bool
    let act: (NextStep) -> Void

    private let stages = ["Import", "Practise", "Upload", "Ask Claude"]

    var body: some View {
        CardBox {
            HStack {
                SectionLabel(text: "NEXT STEP", color: Theme.accent)
                Spacer()
                Text("\(step.stage + 1) of 4").font(.system(size: 12)).foregroundStyle(Theme.muted)
            }
            HStack(spacing: 6) {
                ForEach(0..<4, id: \.self) { k in
                    VStack(alignment: .leading, spacing: 6) {
                        Capsule().fill(k <= step.stage ? Theme.accent : Theme.line).frame(height: 4)
                        Text(stages[k]).font(.system(size: 11, weight: k == step.stage ? .semibold : .regular))
                            .foregroundStyle(k == step.stage ? Theme.text : Theme.muted)
                    }
                }
            }
            Text(title).font(.system(size: 20, weight: .semibold))
            Text(detail).font(.system(size: 15)).foregroundStyle(Theme.text2)
                .fixedSize(horizontal: false, vertical: true)
            if case .askClaude = step {
                PhraseBox()
                Button("I've asked Claude") { act(step) }.buttonStyle(OutlineButtonStyle())
            } else {
                Button { act(step) } label: {
                    HStack(spacing: 8) {
                        if syncing && syncs { ProgressView().tint(Theme.onAccent) } else { Image(systemName: symbol) }
                        Text(buttonTitle)
                    }
                }
                .buttonStyle(AccentButtonStyle())
                .disabled(syncing && syncs)
            }
        }
    }

    /// Only these buttons run a sync; Continue or Start must not wait for the
    /// background check the app does on opening.
    private var syncs: Bool {
        guard linked else { return false }
        switch step {
        case .importEpisodes, .allDone, .upload: return true
        default: return false
        }
    }

    private var title: String {
        switch step {
        case .importEpisodes: return "Import your episodes"
        case .continueEpisode(let p, _): return "Continue \(p.header.title)"
        case .practise(let p): return "Practise \(p.header.title)"
        case .upload(let n): return n == 1 ? "Upload your results" : "Upload \(n) sessions of results"
        case .askClaude: return "Ask Claude to read your results"
        case .allDone: return "Every episode practised"
        }
    }

    private var detail: String {
        switch step {
        case .importEpisodes:
            return linked ? "New episodes arrive in your sync folder by themselves. Pull down or tap below to check now."
                          : "Import .rolesson files — or link an iCloud Drive folder in Settings and they arrive by themselves."
        case .continueEpisode(let p, let progress):
            let done = progress.record.mainItems.count
            return "\(p.header.slug) · drill \(min(done + 1, p.header.drills.count)) of \(p.header.drills.count) · stopped at \(timeString(progress.position))"
        case .practise(let p):
            return "\(p.header.slug) · \(p.header.drills.count) drills · \(Int((p.header.duration / 60).rounded())) min"
        case .upload:
            return linked ? "They go into your sync folder for Claude. Then ask Claude to read them; your next episodes will focus on what you missed."
                          : "Share them to where Claude can read them — or link an iCloud Drive folder in Settings and this happens by itself."
        case .askClaude:
            return "Your results are synced. In Claude, say:"
        case .allDone:
            return "Ask Claude for the next episodes, then import them."
        }
    }

    private var buttonTitle: String {
        switch step {
        case .importEpisodes, .allDone: return linked ? "Check for new episodes" : "Import files"
        case .continueEpisode: return "Continue"
        case .practise: return "Start"
        case .upload: return linked ? "Sync now" : "Share results"
        case .askClaude: return ""
        }
    }

    private var symbol: String {
        switch step {
        case .importEpisodes, .allDone: return "square.and.arrow.down"
        case .continueEpisode, .practise: return "play.fill"
        case .upload: return "arrow.up.doc"
        case .askClaude: return "text.bubble"
        }
    }
}

struct ContinueCard: View {
    let pack: Pack
    let progress: SavedProgress
    let action: () -> Void

    var body: some View {
        HStack(spacing: 14) {
            VStack(alignment: .leading, spacing: 6) {
                SectionLabel(text: "CONTINUE")
                Text(pack.header.title).font(.system(size: 18, weight: .semibold))
                Text("\(pack.header.slug) · drill \(min(progress.record.mainItems.count + 1, pack.header.drills.count)) of \(pack.header.drills.count) · \(timeString(progress.position))")
                    .font(.system(size: 13)).foregroundStyle(Theme.text2)
                ProgressView(value: min(progress.position / max(pack.header.duration, 1), 1))
                    .tint(Theme.accent)
            }
            Button(action: action) {
                Image(systemName: "play.fill").font(.system(size: 22))
                    .frame(width: 56, height: 56)
                    .background(Theme.accent, in: Circle())
                    .foregroundStyle(Theme.onAccent)
            }
            .accessibilityLabel("Continue \(pack.header.title)")
        }
        .padding(16)
        .background(Theme.surface, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 20, style: .continuous).stroke(Theme.line))
    }
}

struct EpisodeRow: View {
    let pack: Pack
    let subtitle: String
    let state: PackStore.EpisodeState
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Text(pack.header.slug.uppercased())
                    .font(.system(size: 12, weight: .bold)).foregroundStyle(Theme.text2)
                    .frame(width: 46, height: 26)
                    .background(Color(hex: 0x1F2530), in: RoundedRectangle(cornerRadius: 8))
                VStack(alignment: .leading, spacing: 2) {
                    Text(pack.header.title).font(.system(size: 15, weight: .semibold)).foregroundStyle(Theme.text)
                    Text(subtitle).font(.system(size: 13)).foregroundStyle(Theme.muted)
                }
                Spacer()
                switch state {
                case .new:
                    Pill(text: "New", foreground: Theme.onAccent, background: Theme.accent)
                case .inProgress:
                    Image(systemName: "play.circle").font(.system(size: 18)).foregroundStyle(Theme.accent)
                case .needsWork:
                    Pill(text: "Needs work", foreground: Color(hex: 0xFFB08F), background: Theme.notQuite.opacity(0.14))
                case .done:
                    Image(systemName: "checkmark.circle.fill").font(.system(size: 18)).foregroundStyle(Theme.right)
                }
            }
            .padding(.horizontal, 14)
            .frame(minHeight: 62)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .accessibilityValue(state.rawValue)
    }
}

enum EpisodeFilter: String, CaseIterable, Identifiable {
    case all = "All", new = "New", inProgress = "In progress", needsWork = "Needs work", done = "Done"
    var id: String { rawValue }
    var state: PackStore.EpisodeState? {
        switch self {
        case .all: return nil
        case .new: return .new
        case .inProgress: return .inProgress
        case .needsWork: return .needsWork
        case .done: return .done
        }
    }
}

enum EpisodeSort: String, CaseIterable, Identifiable {
    case course = "Course order", recent = "Recently played", weakest = "Needs most work"
    var id: String { rawValue }
}

struct ResumeSheet: View {
    let pack: Pack
    let progress: SavedProgress?
    let onContinue: () -> Void
    let onStartOver: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            VStack(alignment: .leading, spacing: 6) {
                SectionLabel(text: "PICK UP WHERE YOU LEFT OFF", color: Theme.accent)
                Text(pack.header.title).font(Theme.display(28))
                if let p = progress {
                    Text("\(pack.header.slug) · stopped \(p.savedAt.formatted(.relative(presentation: .named)))")
                        .font(.system(size: 15)).foregroundStyle(Theme.text2)
                }
            }
            if let p = progress {
                HStack(spacing: 10) {
                    stat("\(min(p.record.mainItems.count + 1, pack.header.drills.count)) / \(pack.header.drills.count)", "drill")
                    stat(timeString(p.position), "of \(timeString(pack.header.duration))")
                    stat("\(p.record.rightFirstTime)", "right so far")
                }
            }
            Button { onContinue() } label: {
                Label("Continue at drill \(min((progress?.record.mainItems.count ?? 0) + 1, pack.header.drills.count))",
                      systemImage: "play.fill")
            }
            .buttonStyle(AccentButtonStyle())
            Button("Start over", action: onStartOver).buttonStyle(OutlineButtonStyle())
            Text("Answers you have given so far are kept either way.")
                .font(.system(size: 13)).foregroundStyle(Theme.muted).frame(maxWidth: .infinity)
        }
        .padding(24)
        .foregroundStyle(Theme.text)
    }

    private func stat(_ value: String, _ label: String) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(value).font(.system(size: 20, weight: .semibold))
            Text(label).font(.system(size: 12)).foregroundStyle(Theme.text2)
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Theme.chip, in: RoundedRectangle(cornerRadius: 14))
    }
}
