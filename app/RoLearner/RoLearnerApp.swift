import SwiftUI

@main
struct RoLearnerApp: App {
    @StateObject private var store = PackStore()
    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            LibraryView().environmentObject(store)
        }
        .onChange(of: scenePhase) { _, phase in
            // Pick up lessons dropped into the app's folder via the Files app.
            if phase == .active {
                store.importDropped()
                store.reload()
            }
        }
    }
}
