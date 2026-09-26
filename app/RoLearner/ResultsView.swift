import SwiftUI
import UniformTypeIdentifiers

struct ResultsView: View {
    @EnvironmentObject private var store: PackStore
    @Environment(\.dismiss) private var dismiss
    @State private var share: ShareItem?
    @State private var importing = false
    @State private var opened: SessionRecord?

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

                VStack(alignment: .leading, spacing: 4) {
                    Text("Sessions").font(.system(size: 17, weight: .semibold))
                    Text("Every answer is kept. A session is one listen-through of an episode; tap it to see each drill, what was heard on each try, and your corrections.")
                        .font(.system(size: 13)).foregroundStyle(Theme.muted)
                }
                .padding(.top, 4)
                if store.sessions.isEmpty {
                    Text("Nothing yet. Practise an episode and it shows up here.").foregroundStyle(Theme.muted)
                } else {
                    VStack(spacing: 0) {
                        ForEach(Array(store.sessions.enumerated()), id: \.element.key) { k, s in
                            Button { opened = s } label: {
                                SessionRow(session: s, stage: store.stage(of: s))
                            }
                            .buttonStyle(.plain)
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
        .sheet(item: $opened) { s in
            SessionDetailView(session: s)
                .presentationBackground(Theme.bg)
        }
        .shakeForLog()
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
            if !wrong.isEmpty {
                Text("\(wrong.count) still wrong: \(wrong.prefix(2).map(\.expected).joined(separator: " · "))\(wrong.count > 2 ? " …" : "")")
                    .font(.system(size: 12)).foregroundStyle(Theme.text2).lineLimit(2)
            }
            Text("See all \(session.items.count) answers ›").font(.system(size: 12, weight: .medium)).foregroundStyle(Theme.accent)
        }
        .padding(.horizontal, 14).padding(.vertical, 12)
        .contentShape(Rectangle())
    }

    private func summary(_ main: [DrillResult]) -> String {
        let when = session.started.formatted(date: .abbreviated, time: .shortened)
        if session.mode == "voice" { return "\(when) · \(session.rightFirstTime) of \(main.count) right first time" }
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

extension SessionRecord: Identifiable {
    var id: String { key }
}

/// One session, every drill: the cue, the answer, each try and what was heard,
/// corrections, and the second-chance round.
struct SessionDetailView: View {
    let session: SessionRecord
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                HStack(spacing: 10) {
                    CircleIconButton(symbol: "chevron.down", label: "Close") { dismiss() }
                    VStack(alignment: .leading, spacing: 2) {
                        Text("\(session.episode.uppercased()) · \(session.title)").font(Theme.display(22))
                        Text(session.started.formatted(date: .abbreviated, time: .shortened))
                            .font(.system(size: 13)).foregroundStyle(Theme.muted)
                    }
                }
                CardBox {
                    Text(headline).font(.system(size: 16, weight: .semibold))
                    Text("“Right first time” counts drills answered correctly on the first try. A second try, the end-of-episode second chance, and answers you corrected are shown below each drill.")
                        .font(.system(size: 13)).foregroundStyle(Theme.text2)
                }
                // by position: going back to a drill can answer it twice in one session
                ForEach(Array(session.items.enumerated()), id: \.offset) { _, it in
                    DrillResultCard(item: it, voice: session.mode == "voice")
                }
            }
            .padding(20)
        }
        .background(Theme.bg.ignoresSafeArea())
        .foregroundStyle(Theme.text)
        .shakeForLog()
    }

    private var headline: String {
        let main = session.mainItems
        if session.mode != "voice" {
            return "\(main.count) drills heard, \(main.filter { $0.outcome == .missed }.count) marked wrong"
        }
        let second = session.items.filter { $0.round == 1 }
        var s = "\(session.rightFirstTime) of \(main.count) answered drills right first time"
        if !second.isEmpty {
            s += "; second chance fixed \(second.filter { $0.outcome == .correct }.count) of \(second.count)"
        }
        return s
    }
}

private struct DrillResultCard: View {
    let item: DrillResult
    let voice: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .top, spacing: 10) {
                Image(systemName: item.outcome == .correct ? "checkmark.circle.fill"
                                  : item.outcome == .unmarked ? "circle" : "xmark.circle.fill")
                    .foregroundStyle(item.outcome.color)
                VStack(alignment: .leading, spacing: 3) {
                    Text(item.cue).font(.system(size: 14)).foregroundStyle(Theme.text2)
                    Text(item.expected).font(.system(size: 16, weight: .semibold))
                }
                Spacer()
                if item.round == 1 {
                    Pill(text: "Second chance", foreground: Color(hex: 0xFFB08F), background: Theme.notQuite.opacity(0.14))
                }
            }
            if voice {
                ForEach(Array(item.attempts.enumerated()), id: \.offset) { k, a in
                    Text("\(k == 0 ? "1st" : "2nd") try: heard \(a.heard.map { "“\($0)”" } ?? "nothing") → \(a.verdict.title)")
                        .font(.system(size: 13)).foregroundStyle(Theme.muted)
                }
            }
            if let c = item.correction {
                Text("You marked it \(c == .correct ? "right" : "wrong")").font(.system(size: 13)).foregroundStyle(Theme.accent)
            }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Theme.surface, in: RoundedRectangle(cornerRadius: 16))
        .overlay(RoundedRectangle(cornerRadius: 16).stroke(Theme.line))
    }
}
