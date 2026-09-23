import SwiftUI
import UniformTypeIdentifiers

struct LibraryView: View {
    @EnvironmentObject private var store: PackStore
    @AppStorage("voiceMode") private var voiceMode = true
    @AppStorage("headsetMic") private var headsetMic = true
    @State private var importing = false
    @State private var active: Pack?

    var body: some View {
        NavigationStack {
            List {
                Section("Episodes") {
                    if store.packs.isEmpty {
                        Text("No episodes yet. Tap Import and pick .rolesson files from Google Drive.")
                            .foregroundStyle(.secondary)
                    }
                    ForEach(store.packs) { pack in
                        Button { active = pack } label: { row(pack) }
                            .foregroundStyle(.primary)
                    }
                    .onDelete { offsets in
                        offsets.map { store.packs[$0] }.forEach(store.delete)
                    }
                }
                Section {
                    Toggle("Listen to my answers", isOn: $voiceMode)
                    Toggle("Use headphone microphone", isOn: $headsetMic)
                } header: {
                    Text("Settings")
                } footer: {
                    Text("With listening off, episodes play straight through and you mark misses yourself. The headphone mic hears you better outdoors but makes Bluetooth playback sound like a phone call.")
                }
                Section {
                    NavigationLink("Results") { ResultsView() }
                }
            }
            .navigationTitle("Română")
            .toolbar {
                Button { importing = true } label: {
                    Label("Import", systemImage: "square.and.arrow.down")
                }
            }
            .fileImporter(isPresented: $importing, allowedContentTypes: [.item],
                          allowsMultipleSelection: true) { result in
                if case .success(let urls) = result { store.importPicked(urls) }
            }
            .fullScreenCover(item: $active) { pack in
                PlayerView(engine: SessionEngine(pack: pack, store: store,
                                                 voiceMode: voiceMode, headsetMic: headsetMic))
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
    }

    private func row(_ pack: Pack) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(pack.header.title).font(.headline)
            Text(subtitle(pack)).font(.subheadline).foregroundStyle(.secondary)
        }
    }

    private func subtitle(_ pack: Pack) -> String {
        var s = "\(pack.header.slug) · \(pack.header.drills.count) drills"
        if let last = store.lastScore(for: pack.header.slug) { s += " · last \(last)" }
        return s
    }
}

struct PlayerView: View {
    @StateObject private var engine: SessionEngine
    @Environment(\.dismiss) private var dismiss

    init(engine: @autoclosure @escaping () -> SessionEngine) {
        _engine = StateObject(wrappedValue: engine())
    }

    var body: some View {
        VStack(spacing: 20) {
            HStack {
                Button("Close") { engine.stop(); dismiss() }
                Spacer()
                Text(engine.inRetry ? "Second chance" : "\(engine.done) / \(engine.total)")
                    .monospacedDigit()
                    .foregroundStyle(.secondary)
            }
            Text(engine.pack.header.title)
                .font(.title2.bold())
                .frame(maxWidth: .infinity, alignment: .leading)
            if let note = engine.note {
                Text(note).font(.footnote).foregroundStyle(.orange)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            Spacer()
            status
            Spacer()
            HStack(spacing: 12) {
                Button { engine.override(.missed) } label: {
                    Label("Mark wrong", systemImage: "xmark").frame(maxWidth: .infinity)
                }
                .tint(.red)
                if engine.voiceMode {
                    Button { engine.override(.correct) } label: {
                        Label("It was right", systemImage: "checkmark").frame(maxWidth: .infinity)
                    }
                    .tint(.green)
                }
            }
            .buttonStyle(.bordered)
            .controlSize(.large)
            Button { engine.togglePause() } label: {
                Image(systemName: engine.phase == .paused ? "play.fill" : "pause.fill")
                    .font(.largeTitle)
                    .frame(maxWidth: .infinity, minHeight: 64)
            }
            .buttonStyle(.borderedProminent)
            .disabled(engine.phase == .finished)
        }
        .padding()
        .task { await engine.start() }
    }

    @ViewBuilder private var status: some View {
        VStack(spacing: 12) {
            switch engine.phase {
            case .idle:
                ProgressView()
            case .listening:
                Label("Listening…", systemImage: "waveform").font(.title3).foregroundStyle(.blue)
                if let cue = engine.lastCue {
                    Text(cue).font(.title3).multilineTextAlignment(.center)
                }
            case .finished:
                Text("Done").font(.largeTitle.bold())
                if engine.voiceMode {
                    Text("\(engine.correctCount) of \(engine.total) right first time").font(.title3)
                }
            default:
                if let v = engine.lastVerdict {
                    Text(label(v)).font(.title.bold()).foregroundStyle(color(v))
                    if let e = engine.lastExpected {
                        Text(e).font(.title3).multilineTextAlignment(.center)
                    }
                    Text("Heard: \(engine.lastHeard ?? "nothing")")
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)
                } else if let cue = engine.lastCue, !engine.voiceMode {
                    Text(cue).font(.title3).multilineTextAlignment(.center)
                    Text("Missed it? Tap Mark wrong.").foregroundStyle(.secondary)
                }
            }
        }
    }

    private func label(_ v: Verdict) -> String {
        switch v {
        case .correct: return "Right"
        case .close: return "Close"
        case .missed: return "Not quite"
        case .noAnswer: return "Didn't hear you"
        case .unmarked: return ""
        }
    }

    private func color(_ v: Verdict) -> Color {
        switch v {
        case .correct: return .green
        case .close: return .orange
        case .missed, .noAnswer: return .red
        case .unmarked: return .secondary
        }
    }
}

struct ResultsView: View {
    @EnvironmentObject private var store: PackStore
    @State private var exportURL: URL?

    var body: some View {
        List {
            if let url = exportURL {
                ShareLink(item: url) {
                    Label("Share all results (Save to Files → Drive)", systemImage: "square.and.arrow.up")
                }
            }
            ForEach(store.sessions, id: \.started) { s in
                SessionRow(session: s)
            }
        }
        .navigationTitle("Results")
        .onAppear { exportURL = store.exportAll() }
    }
}

private struct SessionRow: View {
    let session: SessionRecord

    var body: some View {
        let main = session.items.filter { !$0.retry }
        let wrong = main.filter { $0.verdict != .correct && $0.verdict != .unmarked }
        VStack(alignment: .leading, spacing: 4) {
            Text("\(session.episode) · \(session.title)").font(.headline)
            Text("\(main.filter { $0.verdict == .correct }.count)/\(main.count) right · "
                 + session.started.formatted(date: .abbreviated, time: .shortened))
                .font(.subheadline)
                .foregroundStyle(.secondary)
            ForEach(wrong) { it in
                Text("✗ \(it.expected) — heard: \(it.heard ?? "nothing")").font(.caption)
            }
        }
    }
}
