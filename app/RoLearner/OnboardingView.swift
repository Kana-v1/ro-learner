import SwiftUI
import UniformTypeIdentifiers

/// First launch: permissions, a way to get episodes in, and what to expect with
/// the phone in a pocket.
struct OnboardingView: View {
    @EnvironmentObject private var store: PackStore
    let onDone: () -> Void
    @State private var permission: Bool?
    @State private var linking = false
    @State private var importing = false

    private var hasEpisodes: Bool { !store.packs.isEmpty || store.linkedFolder != nil }

    var body: some View {
        VStack(alignment: .leading, spacing: 26) {
            HStack(spacing: 12) {
                Text("ă").font(Theme.display(28)).foregroundStyle(Theme.notQuite)
                    .frame(width: 48, height: 48)
                    .background(Theme.onNotQuite, in: RoundedRectangle(cornerRadius: 13))
                Text("Vorbește").font(Theme.display(22))
            }
            VStack(alignment: .leading, spacing: 12) {
                Text("Practise Romanian with your phone in your pocket.")
                    .font(Theme.display(32)).fixedSize(horizontal: false, vertical: true)
                Text("Episodes stop after each question and listen for your answer. You hear what to do at every step.")
                    .font(.system(size: 16)).foregroundStyle(Theme.text2)
            }
            VStack(alignment: .leading, spacing: 18) {
                step(1, done: permission == true, active: permission == nil,
                     "Allow microphone and speech recognition",
                     permission == false ? "Off for now: episodes play through and you mark misses yourself. You can allow it later in Settings."
                                         : "Only the text of your answers is kept, never the audio.")
                step(2, done: hasEpisodes, active: permission != nil && !hasEpisodes,
                     "Link your Google Drive folder",
                     "New episodes arrive there, and your results go back there for Claude.")
                step(3, done: false, active: false, "Put the phone away",
                     "A rising chime means it's your turn. Every verdict is spoken aloud.")
            }
            Spacer()
            VStack(spacing: 10) {
                if permission == nil {
                    Button {
                        Task { permission = await Listener.requestPermissions() }
                    } label: { Label("Allow microphone & speech", systemImage: "mic.fill") }
                    .buttonStyle(AccentButtonStyle())
                } else if !hasEpisodes {
                    Button { linking = true } label: { Label("Link Drive folder", systemImage: "folder") }
                        .buttonStyle(AccentButtonStyle())
                    Button("Import files instead") { importing = true }
                        .font(.system(size: 15, weight: .medium)).foregroundStyle(Theme.text2)
                        .frame(minHeight: 44)
                } else {
                    Button(action: onDone) { Label("Start practising", systemImage: "play.fill") }
                        .buttonStyle(AccentButtonStyle())
                }
                Button("Not now", action: onDone)
                    .font(.system(size: 15, weight: .medium)).foregroundStyle(Theme.muted)
                    .frame(minHeight: 44)
            }
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 28)
        .background(Theme.bg.ignoresSafeArea())
        .foregroundStyle(Theme.text)
        .fileImporter(isPresented: $linking, allowedContentTypes: [.folder]) { result in
            if case .success(let url) = result {
                store.linkFolder(url)
                Task { await store.sync() }
            }
        }
        .background(
            Color.clear.fileImporter(isPresented: $importing, allowedContentTypes: [.item],
                                     allowsMultipleSelection: true) { result in
                if case .success(let urls) = result { store.importPicked(urls) }
            }
        )
    }

    private func step(_ n: Int, done: Bool, active: Bool, _ title: String, _ detail: String) -> some View {
        HStack(alignment: .top, spacing: 14) {
            NumberBadge(number: n, active: active, done: done)
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.system(size: 16, weight: .semibold))
                Text(detail).font(.system(size: 14)).foregroundStyle(Theme.text2)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}
