import SwiftUI

/// A quick note for Claude, written (or dictated with the keyboard's mic)
/// the moment something is off, so it isn't forgotten by the end of the walk.
/// From the player it carries the drill on screen and the last few answered;
/// it goes up with the next sync to the data repo's feedback/ folder.
struct FeedbackSheet: View {
    /// What the note is about, shown at the top ("Drill 41/84 · My sister is thin.").
    let about: String?
    var kinds: [(id: String, label: String)] = FeedbackSheet.playerKinds
    let onSend: (_ kind: String, _ text: String) -> Void

    static let playerKinds: [(id: String, label: String)] = [("wrong_answer", "Wrong answer"), ("not_heard", "Didn't hear me"),
                              ("audio", "Audio"), ("idea", "Idea"), ("other", "Other")]
    static let homeKinds: [(id: String, label: String)] = [("idea", "Idea"), ("app", "App problem"), ("other", "Other")]

    @Environment(\.dismiss) private var dismiss
    @State private var kind: String?
    @State private var text = ""
    @FocusState private var typing: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            VStack(alignment: .leading, spacing: 6) {
                SectionLabel(text: "FEEDBACK FOR CLAUDE", color: Theme.accent)
                if let about {
                    Text(about).font(.system(size: 15)).foregroundStyle(Theme.text2).lineLimit(3)
                }
            }
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(kinds.indices, id: \.self) { i in
                        let k = kinds[i]
                        let on = (kind ?? kinds[0].id) == k.id
                        Button { kind = k.id } label: {
                            Text(k.label).font(.system(size: 14, weight: .semibold))
                                .padding(.horizontal, 14).frame(height: 34)
                                .foregroundStyle(on ? Theme.onAccent : Theme.text2)
                                .background(on ? Theme.accent : Theme.surface, in: Capsule())
                                .overlay(Capsule().stroke(on ? Color.clear : Theme.line))
                        }
                    }
                }
            }
            TextField("What happened? (the keyboard's mic works too)", text: $text, axis: .vertical)
                .lineLimit(3...8)
                .focused($typing)
                .padding(12)
                .background(Theme.surface, in: RoundedRectangle(cornerRadius: 12))
                .overlay(RoundedRectangle(cornerRadius: 12).stroke(Theme.line))
            Button("Send") {
                onSend(kind ?? kinds[0].id, text.trimmingCharacters(in: .whitespacesAndNewlines))
                dismiss()
            }
            .buttonStyle(AccentButtonStyle())
            Text("Saved with where you are in the episode, and sent with the next sync.")
                .font(.system(size: 12)).foregroundStyle(Theme.muted)
            Spacer(minLength: 0)
        }
        .padding(20)
        .foregroundStyle(Theme.text)
        .onAppear { typing = true }
    }
}
