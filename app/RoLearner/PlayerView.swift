import SwiftUI

struct PlayerView: View {
    @StateObject private var engine: SessionEngine
    @ObservedObject private var store: PackStore
    @Environment(\.dismiss) private var dismiss
    @Environment(\.scenePhase) private var scenePhase
    @State private var showChapters = false
    @State private var scrub: Double?
    @State private var share: ShareItem?

    init(launch: PlayerLaunch, store: PackStore, voiceMode: Bool, headsetMic: Bool) {
        _engine = StateObject(wrappedValue: SessionEngine(pack: launch.pack, store: store, voiceMode: voiceMode,
                                                         headsetMic: headsetMic, resume: launch.resume))
        self.store = store
    }

    var body: some View {
        VStack(spacing: 16) {
            topBar
            if engine.phase == .finished {
                FinishedPanel(engine: engine, store: store, onUpload: upload, onClose: close)
            } else {
                chip
                if let note = engine.note {
                    Text(note).font(.system(size: 13)).foregroundStyle(Theme.accent)
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
                status.frame(maxHeight: .infinity)
                corrections
                if !engine.inRound { scrubber }
                controls
            }
        }
        .padding(.horizontal, 20)
        .padding(.top, 12)
        .padding(.bottom, 20)
        .background(Theme.bg.ignoresSafeArea())
        .foregroundStyle(Theme.text)
        .task { await engine.start() }
        .onDisappear { engine.close() }      // swiped down: same as the X
        .shakeForLog()
        .onChange(of: scenePhase) { _, p in
            if p != .active { engine.persist() }
        }
        .sheet(isPresented: $showChapters) {
            ChaptersSheet(engine: engine)
                .presentationDetents([.medium, .large])
                .presentationBackground(Theme.raised)
        }
        .sheet(item: $share) { item in
            ShareSheet(items: [item.url]) { done in
                if done { store.markSent(item.keys) }
                share = nil
            }
            .presentationDetents([.medium, .large])
        }
    }

    private func close() {
        engine.close()
        dismiss()
    }

    private func upload() {
        if store.linkedFolder != nil {
            Task { await store.sync() }
        } else {
            share = store.exportUnsent()
        }
    }

    // MARK: sections

    private var topBar: some View {
        HStack(spacing: 12) {
            CircleIconButton(symbol: "xmark", label: "Close", action: close)
            Spacer()
            VStack(spacing: 2) {
                Text(engine.pack.header.title).font(.system(size: 15, weight: .semibold)).lineLimit(1)
                Text(engine.pack.header.slug.uppercased()).font(.system(size: 12)).foregroundStyle(Theme.muted)
            }
            Spacer()
            Text(engine.phase == .finished ? "" : engine.drillLabel)
                .font(.system(size: 15, weight: .semibold)).monospacedDigit()
                .frame(width: 44, alignment: .trailing)
        }
    }

    @ViewBuilder private var chip: some View {
        if engine.inRound {
            Pill(text: "Second chance · \(min(engine.roundDone + 1, engine.roundTotal)) of \(engine.roundTotal)",
                 symbol: "arrow.counterclockwise", foreground: Color(hex: 0xFFB08F),
                 background: Theme.notQuite.opacity(0.14))
        } else if engine.phase == .secondTry || (engine.phase == .listening && engine.attempt == 2) {
            Pill(text: "Second try", symbol: "arrow.counterclockwise",
                 foreground: Color(hex: 0xFFB08F), background: Theme.notQuite.opacity(0.14))
        } else {
            Button { showChapters = true } label: {
                Label("\(engine.currentChapter?.name ?? "Chapters") · Chapters", systemImage: "list.bullet")
                    .font(.system(size: 14, weight: .medium))
                    .padding(.horizontal, 14).frame(height: 36)
                    .overlay(Capsule().stroke(Theme.line))
            }
            .foregroundStyle(Theme.text2)
        }
    }

    @ViewBuilder private var status: some View {
        VStack(spacing: 18) {
            switch engine.phase {
            case .idle:
                ProgressView().tint(Theme.accent)
            case .listening:
                StatusDisc(color: Theme.accent, ink: Theme.onAccent, symbol: "mic.fill")
                Text(engine.attempt == 2 ? "Once more" : "Your turn")
                    .font(Theme.display(44)).foregroundStyle(Theme.accent)
                if let d = engine.current { cueBlock(d.cue) }
                hearing
            case .secondTry:
                StatusDisc(color: Theme.notQuite, ink: Theme.onNotQuite, symbol: "arrow.counterclockwise")
                Text(engine.lastVerdict == .noAnswer ? "Didn't catch that" : "Not quite")
                    .font(Theme.display(40)).foregroundStyle(Theme.notQuite)
                    .multilineTextAlignment(.center)
                if let h = engine.lastHeard {
                    Text("Heard: \(h)").font(.system(size: 15)).italic().foregroundStyle(Theme.text2)
                        .multilineTextAlignment(.center)
                }
                // The answer stays hidden here: showing it would turn the retry
                // into reading instead of remembering.
                Text("The question plays again, then it's your turn once more.")
                    .font(.system(size: 15)).multilineTextAlignment(.center)
            case .feedback, .playing, .paused:
                if let v = engine.lastVerdict, v != .unmarked, let d = engine.current {
                    StatusDisc(color: v.color, ink: v.ink, symbol: v.symbol)
                    Text(v.title).font(Theme.display(44)).foregroundStyle(v.color)
                    answerBlock(d.expected)
                    if v == .close, let hint = engine.lastHint, !hint.isEmpty {
                        Text(hint).font(.system(size: 16, weight: .semibold)).foregroundStyle(Theme.accent)
                            .multilineTextAlignment(.center)
                    }
                    if engine.voiceMode {
                        Text("Heard: \(engine.lastHeard ?? "nothing")").font(.system(size: 15))
                            .foregroundStyle(Theme.text2).multilineTextAlignment(.center)
                    }
                } else if !engine.voiceMode, let d = engine.current {
                    cueBlock(d.cue)
                    Text("Missed it? Tap Mark wrong.").font(.system(size: 14)).foregroundStyle(Theme.muted)
                } else {
                    Image(systemName: engine.phase == .paused ? "pause.circle" : "waveform")
                        .font(.system(size: 56, weight: .light)).foregroundStyle(Theme.muted)
                    Text(engine.currentChapter?.name ?? engine.pack.header.title)
                        .font(Theme.display(28)).multilineTextAlignment(.center)
                    Text(engine.phase == .paused ? "Paused" : "Listen")
                        .font(.system(size: 15)).foregroundStyle(Theme.muted)
                }
            case .finished:
                EmptyView()
            }
        }
        .frame(maxWidth: .infinity)
    }

    private func cueBlock(_ cue: String) -> some View {
        VStack(spacing: 6) {
            SectionLabel(text: engine.attempt == 2 ? "ONCE MORE, IN ROMANIAN" : "SAY IT IN ROMANIAN")
            Text(cue).font(.system(size: 22)).multilineTextAlignment(.center)
        }
    }

    private func answerBlock(_ answer: String) -> some View {
        VStack(spacing: 6) {
            SectionLabel(text: "ANSWER")
            Text(answer).font(.system(size: 24, weight: .semibold)).multilineTextAlignment(.center)
        }
    }

    private var hearing: some View {
        VStack(alignment: .leading, spacing: 4) {
            SectionLabel(text: "HEARING")
            Text(engine.liveHeard ?? "…").font(.system(size: 17)).italic().foregroundStyle(Theme.text2)
        }
        .padding(.horizontal, 14).padding(.vertical, 12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Theme.surface, in: RoundedRectangle(cornerRadius: 16))
        .overlay(RoundedRectangle(cornerRadius: 16).stroke(Theme.line))
    }

    @ViewBuilder private var corrections: some View {
        if engine.voiceMode {
            if engine.phase == .secondTry || (engine.phase == .listening && engine.attempt == 2) {
                HStack(spacing: 10) {
                    Button { engine.correct(.correct) } label: {
                        Label("It was right", systemImage: "checkmark")
                    }
                    Button("Skip the retry") { engine.skipRetry() }
                }
                .buttonStyle(OutlineButtonStyle())
            } else if let v = engine.lastVerdict, v != .unmarked,
                      engine.phase == .feedback || engine.phase == .playing || engine.phase == .paused {
                if v == .correct {
                    Button { engine.correct(.missed) } label: { Label("Mark wrong", systemImage: "xmark") }
                        .buttonStyle(OutlineButtonStyle())
                } else {
                    Button { engine.correct(.correct) } label: { Label("It was right", systemImage: "checkmark") }
                        .buttonStyle(OutlineButtonStyle())
                }
            }
        } else if engine.current != nil {
            Button { engine.correct(.missed) } label: { Label("Mark wrong", systemImage: "xmark") }
                .buttonStyle(OutlineButtonStyle())
        }
    }

    private var scrubber: some View {
        VStack(spacing: 2) {
            ZStack {
                GeometryReader { g in
                    ForEach(engine.chapters) { c in
                        Rectangle().fill(Theme.tick).frame(width: 2, height: 10)
                            .position(x: g.size.width * c.start / max(engine.duration, 1), y: g.size.height / 2)
                    }
                }
                .allowsHitTesting(false)
                Slider(value: Binding(get: { scrub ?? engine.position }, set: { scrub = $0 }),
                       in: 0...max(engine.duration, 1),
                       onEditingChanged: { editing in
                           if !editing, let t = scrub {
                               engine.seek(to: t)
                               scrub = nil
                           }
                       })
                .tint(Theme.accent)
                .accessibilityLabel("Position")
            }
            .frame(height: 30)
            HStack {
                Text(timeString(scrub ?? engine.position))
                Spacer()
                Text(timeString(engine.duration))
            }
            .font(.system(size: 12)).monospacedDigit().foregroundStyle(Theme.muted)
        }
    }

    private var controls: some View {
        HStack {
            controlButton("backward.end.fill", "Previous drill") { engine.previousDrill() }
            Spacer()
            controlButton("gobackward.10", "Back 10 seconds") { engine.skip(-10) }
                .disabled(engine.inRound).opacity(engine.inRound ? 0.3 : 1)
            Spacer()
            Button { engine.togglePause() } label: {
                Image(systemName: engine.phase == .paused ? "play.fill" : "pause.fill")
                    .font(.system(size: 28, weight: .semibold))
                    .frame(width: 72, height: 72)
                    .background(Theme.accent, in: Circle())
                    .foregroundStyle(Theme.onAccent)
            }
            .accessibilityLabel(engine.phase == .paused ? "Play" : "Pause")
            Spacer()
            controlButton("goforward.10", "Forward 10 seconds") { engine.skip(10) }
                .disabled(engine.inRound).opacity(engine.inRound ? 0.3 : 1)
            Spacer()
            controlButton("forward.end.fill", "Next drill") { engine.nextDrill() }
        }
    }

    private func controlButton(_ symbol: String, _ label: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Image(systemName: symbol).font(.system(size: 24, weight: .medium)).frame(width: 48, height: 48)
        }
        .foregroundStyle(Theme.text)
        .accessibilityLabel(label)
    }
}

struct ChaptersSheet: View {
    @ObservedObject var engine: SessionEngine
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                Text("Chapters").font(Theme.display(26))
                Spacer()
                CircleIconButton(symbol: "xmark", label: "Close chapters") { dismiss() }
            }
            ScrollView {
                VStack(spacing: 2) {
                    ForEach(engine.chapters) { c in
                        let isCurrent = engine.currentChapter?.id == c.id
                        Button {
                            engine.jump(to: c)
                            dismiss()
                        } label: {
                            HStack(spacing: 12) {
                                if isCurrent { Circle().fill(Theme.accent).frame(width: 8, height: 8) }
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(c.name).font(.system(size: 16, weight: isCurrent ? .semibold : .regular))
                                    if isCurrent {
                                        Text("Now").font(.system(size: 12)).foregroundStyle(Theme.accent)
                                    } else if c.drillCount > 0 {
                                        Text("\(c.drillCount) drills").font(.system(size: 12)).foregroundStyle(Theme.muted)
                                    }
                                }
                                Spacer()
                                Text(timeString(c.start)).font(.system(size: 14)).monospacedDigit().foregroundStyle(Theme.muted)
                            }
                            .padding(.horizontal, 12)
                            .frame(minHeight: 54)
                            .background(isCurrent ? Color(hex: 0x262D39) : Color.clear, in: RoundedRectangle(cornerRadius: 12))
                            .contentShape(Rectangle())
                        }
                        .buttonStyle(.plain)
                        .foregroundStyle(Theme.text)
                    }
                }
            }
        }
        .padding(20)
        .foregroundStyle(Theme.text)
    }
}

struct FinishedPanel: View {
    @ObservedObject var engine: SessionEngine
    @ObservedObject var store: PackStore
    let onUpload: () -> Void
    let onClose: () -> Void

    private var uploaded: Bool {
        store.status.sent[engine.record.key] != nil || store.status.analyzed.contains(engine.record.key)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                Text("Episode done").font(Theme.display(36))
                if engine.voiceMode {
                    VStack(alignment: .leading, spacing: 4) {
                        HStack(alignment: .firstTextBaseline, spacing: 10) {
                            (Text("\(engine.rightFirstTime)").foregroundStyle(Theme.right)
                             + Text("/\(engine.total)").foregroundStyle(Theme.tick))
                                .font(Theme.display(56))
                            Text("right first time").font(.system(size: 15)).foregroundStyle(Theme.text2)
                        }
                        if engine.roundTotal > 0 {
                            Text("Second chance fixed \(engine.fixedInRound) of \(engine.roundTotal)")
                                .font(.system(size: 14)).foregroundStyle(Theme.text2)
                        }
                    }
                } else {
                    Text("\(engine.markedWrong) marked wrong").font(.system(size: 17)).foregroundStyle(Theme.text2)
                }

                let todo = engine.stillToWorkOn
                if !todo.isEmpty {
                    CardBox {
                        SectionLabel(text: "STILL TO WORK ON")
                        ForEach(todo.prefix(6)) { it in
                            Text(it.expected).font(.system(size: 15))
                        }
                    }
                }

                CardBox {
                    SectionLabel(text: "WHAT TO DO NOW", color: Theme.accent)
                    HStack(alignment: .top, spacing: 12) {
                        NumberBadge(number: 1, active: !uploaded, done: uploaded)
                        VStack(alignment: .leading, spacing: 10) {
                            Text(uploaded ? "Results are synced for Claude" : "Send results to Claude")
                                .font(.system(size: 16, weight: .semibold))
                            if !uploaded {
                                Button(action: onUpload) {
                                    HStack(spacing: 8) {
                                        if store.syncing { ProgressView().tint(Theme.onAccent) }
                                        else { Image(systemName: "arrow.up.doc") }
                                        Text(store.linkedFolder != nil ? "Sync now" : "Share results")
                                    }
                                }
                                .buttonStyle(AccentButtonStyle())
                                .disabled(store.syncing)
                            }
                        }
                    }
                    HStack(alignment: .top, spacing: 12) {
                        NumberBadge(number: 2, active: uploaded)
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Tell Claude").font(.system(size: 16, weight: .semibold))
                            PhraseBox()
                        }
                    }
                    HStack(alignment: .top, spacing: 12) {
                        NumberBadge(number: 3)
                        Text("Claude adjusts your next episodes. What you missed comes back sooner.")
                            .font(.system(size: 14)).foregroundStyle(Theme.text2)
                    }
                }

                Button("Back to episodes", action: onClose).buttonStyle(OutlineButtonStyle())
            }
            .padding(.top, 8)
        }
    }
}
