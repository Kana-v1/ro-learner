import SwiftUI
import UniformTypeIdentifiers

struct ResultsView: View {
    @EnvironmentObject private var store: PackStore
    @Environment(\.dismiss) private var dismiss
    @State private var share: ShareItem?
    @State private var importing = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                HStack(spacing: 10) {
                    CircleIconButton(symbol: "chevron.down", label: "Close") { dismiss() }
                    Text("Results").font(Theme.display(30))
                    Spacer()
                    Button("Import notes") { importing = true }
                        .font(.system(size: 14, weight: .medium)).foregroundStyle(Theme.text2)
                }

                if !store.unsent.isEmpty {
                    HStack(spacing: 12) {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(store.unsent.count == 1 ? "1 session not sent" : "\(store.unsent.count) sessions not sent")
                                .font(.system(size: 16, weight: .semibold))
                            Text("Claude can only use what is on Drive.").font(.system(size: 13)).foregroundStyle(Theme.text2)
                        }
                        Spacer()
                        Button {
                            if store.linkedFolder != nil { Task { await store.sync() } }
                            else { share = store.exportUnsent() }
                        } label: {
                            Label(store.linkedFolder != nil ? "Sync" : "Upload", systemImage: "arrow.up.doc")
                                .font(.system(size: 15, weight: .semibold))
                                .padding(.horizontal, 14).frame(height: 44)
                                .background(Theme.accent, in: RoundedRectangle(cornerRadius: 12))
                                .foregroundStyle(Theme.onAccent)
                        }
                    }
                    .padding(14)
                    .background(Theme.surface, in: RoundedRectangle(cornerRadius: 18))
                    .overlay(RoundedRectangle(cornerRadius: 18).stroke(Theme.line))
                }

                if let note = store.notes.first, let report = note.report, !report.isEmpty {
                    CardBox(fill: Theme.infoCard, stroke: Theme.infoLine) {
                        SectionLabel(text: "FROM CLAUDE · \(note.created.formatted(date: .abbreviated, time: .omitted).uppercased())",
                                     color: Theme.info)
                        Text(report).font(.system(size: 15))
                    }
                }

                Text("Sessions").font(.system(size: 17, weight: .semibold)).padding(.top, 4)
                if store.sessions.isEmpty {
                    Text("Nothing yet. Practise an episode and it shows up here.").foregroundStyle(Theme.muted)
                } else {
                    VStack(spacing: 0) {
                        ForEach(Array(store.sessions.enumerated()), id: \.element.key) { k, s in
                            SessionRow(session: s, stage: store.stage(of: s))
                                .overlay(alignment: .top) {
                                    if k > 0 { Rectangle().fill(Color(hex: 0x232934)).frame(height: 1) }
                                }
                        }
                    }
                    .background(Theme.surface, in: RoundedRectangle(cornerRadius: 18))
                    .overlay(RoundedRectangle(cornerRadius: 18).stroke(Theme.line))
                }
            }
            .padding(20)
        }
        .background(Theme.bg.ignoresSafeArea())
        .foregroundStyle(Theme.text)
        .fileImporter(isPresented: $importing, allowedContentTypes: [.item], allowsMultipleSelection: true) { result in
            if case .success(let urls) = result { store.importPicked(urls) }
        }
        .sheet(item: $share) { item in
            ShareSheet(items: [item.url]) { done in
                if done { store.markSent(item.keys) }
                share = nil
            }
            .presentationDetents([.medium, .large])
        }
    }
}

private struct SessionRow: View {
    let session: SessionRecord
    let stage: PackStore.Stage

    var body: some View {
        let main = session.mainItems
        let wrong = main.filter { $0.outcome != .correct && $0.outcome != .unmarked }
        VStack(alignment: .leading, spacing: 6) {
            HStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 2) {
                    Text("\(session.episode.uppercased()) · \(session.title)").font(.system(size: 15, weight: .semibold))
                    Text(summary(main)).font(.system(size: 13)).foregroundStyle(Theme.muted)
                }
                Spacer()
                pill
            }
            ForEach(wrong.prefix(4)) { it in
                Text("✗ \(it.expected) — heard: \(it.heard ?? "nothing")")
                    .font(.system(size: 12)).foregroundStyle(Theme.text2)
            }
        }
        .padding(.horizontal, 14).padding(.vertical, 12)
    }

    private func summary(_ main: [DrillResult]) -> String {
        let when = session.started.formatted(date: .abbreviated, time: .shortened)
        if session.mode == "voice" { return "\(when) · \(session.rightFirstTime) of \(main.count) right" }
        return "\(when) · \(main.filter { $0.outcome == .missed }.count) marked wrong"
    }

    @ViewBuilder private var pill: some View {
        switch stage {
        case .inProgress:
            Pill(text: "In progress", foreground: Theme.text2, background: Theme.chip)
        case .notSent:
            Pill(text: "Not sent", foreground: Theme.accent, background: Theme.accent.opacity(0.14))
        case .sent:
            Pill(text: "Sent", foreground: Color(hex: 0xC3CAD5), background: Color(hex: 0x262D39))
        case .analyzed:
            Pill(text: "Analysed", symbol: "checkmark", foreground: Theme.info, background: Theme.info.opacity(0.14))
        }
    }
}
