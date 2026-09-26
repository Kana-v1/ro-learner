import SwiftUI

@main
struct RoLearnerApp: App {
    @StateObject private var store = PackStore()
    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            HomeView()
                .environmentObject(store)
                .preferredColorScheme(.dark)
                .tint(Theme.accent)
        }
        .onChange(of: scenePhase) { _, phase in
            // Coming back to the app is when new lessons and notes get picked up,
            // from the Files-app folder and from the linked Drive folder.
            if phase == .active {
                store.importDropped()
                store.reload()
                Task { await store.sync() }
            }
        }
    }
}
