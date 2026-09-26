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
    @AppStorage("headsetMic") private var headsetMic = true
    @AppStorage("onboarded") private var onboarded = false
    @State private var importing = false
    @State private var linking = false
    @State private var launch: PlayerLaunch?
    @State private var resumeCandidate: Pack?
    @State private var pendingLaunch: PlayerLaunch?
    @State private var share: ShareItem?
    @State private var showResults = false

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
        .fullScreenCover(item: $launch) { l in
            PlayerView(launch: l, store: store, voiceMode: voiceMode, headsetMic: headsetMic)
                .environmentObject(store)
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

    private var episodes: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Episodes").font(.system(size: 17, weight: .semibold))
                Spacer()
                Button { importing = true } label: {
                    Label("Import", systemImage: "plus").font(.system(size: 14, weight: .medium))
                        .padding(.horizontal, 12).frame(height: 36)
                        .overlay(Capsule().stroke(Theme.line))
                }
                .foregroundStyle(Theme.text)
            }
            if store.packs.isEmpty {
                Text("No episodes yet.").foregroundStyle(Theme.muted)
            } else {
                VStack(spacing: 0) {
                    ForEach(Array(store.packs.enumerated()), id: \.element.id) { k, pack in
                        EpisodeRow(pack: pack, subtitle: store.subtitle(for: pack), isNew: store.isNew(pack)) {
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
        }
    }

    private var settings: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Settings").font(.system(size: 17, weight: .semibold)).padding(.top, 8)
            CardBox {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text("Google Drive folder").font(.system(size: 15, weight: .semibold))
                            Text(driveStatus).font(.system(size: 13)).foregroundStyle(Theme.muted)
                        }
                        Spacer()
                        if store.syncing { ProgressView().tint(Theme.accent) }
                    }
                    if store.linkedFolder == nil {
                        Button("Link Drive folder") {
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
                    Text("Pick a folder holding lessons/. New episodes are picked up from it and your results are written into results/ whenever the app is open.")
                        .font(.system(size: 12)).foregroundStyle(Theme.muted)
                }
                Divider().overlay(Theme.line)
                Toggle("Listen to my answers", isOn: $voiceMode).tint(Theme.accent)
                Toggle("Use headphone microphone", isOn: $headsetMic).tint(Theme.accent)
                Text("With listening off, episodes play straight through and you mark misses yourself. The headphone mic hears you better outdoors but makes Bluetooth playback sound like a phone call.")
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
                        if syncing { ProgressView().tint(Theme.onAccent) } else { Image(systemName: symbol) }
                        Text(buttonTitle)
                    }
                }
                .buttonStyle(AccentButtonStyle())
                .disabled(syncing)
            }
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
            return linked ? "New episodes arrive in your Drive folder's lessons/. Pull down or tap below to check for them."
                          : "Pick the .rolesson files from Google Drive. You can choose several at once."
        case .continueEpisode(let p, let progress):
            let done = progress.record.mainItems.count
            return "\(p.header.slug) · drill \(min(done + 1, p.header.drills.count)) of \(p.header.drills.count) · stopped at \(timeString(progress.position))"
        case .practise(let p):
            return "\(p.header.slug) · \(p.header.drills.count) drills · \(Int((p.header.duration / 60).rounded())) min"
        case .upload:
            return linked ? "They go into your Drive folder's results/. Then ask Claude to read them; your next episodes will focus on what you missed."
                          : "Send them to Google Drive, then ask Claude to read them. Your next episodes will focus on what you missed."
        case .askClaude:
            return "Your results are on Drive. In Claude, say:"
        case .allDone:
            return "Ask Claude for the next episodes, then import them."
        }
    }

    private var buttonTitle: String {
        switch step {
        case .importEpisodes, .allDone: return linked ? "Check Drive for episodes" : "Import from Drive"
        case .continueEpisode: return "Continue"
        case .practise: return "Start"
        case .upload: return linked ? "Sync to Drive" : "Upload to Drive"
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
    let isNew: Bool
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
                if isNew {
                    Pill(text: "New", foreground: Theme.onAccent, background: Theme.accent)
                } else {
                    Image(systemName: "chevron.right").font(.system(size: 14, weight: .semibold)).foregroundStyle(Theme.muted)
                }
            }
            .padding(.horizontal, 14)
            .frame(minHeight: 62)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }
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
