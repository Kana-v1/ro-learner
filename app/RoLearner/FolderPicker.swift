import SwiftUI
import UIKit
import UniformTypeIdentifiers

/// The system document picker in folder mode, used directly. SwiftUI's
/// .fileImporter only reliably allows one per screen, and the "import files"
/// picker on the same screen silently swallowed the folder one — tapping
/// "Link Drive folder" did nothing. This is also the route Apple documents for
/// giving an app access to a folder in another app (Google Drive, iCloud).
struct FolderPicker: UIViewControllerRepresentable {
    let onPick: (URL) -> Void
    let onCancel: () -> Void

    func makeCoordinator() -> Coordinator { Coordinator(onPick: onPick, onCancel: onCancel) }

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let vc = UIDocumentPickerViewController(forOpeningContentTypes: [.folder])
        vc.delegate = context.coordinator
        vc.allowsMultipleSelection = false
        Log.write("folder picker: opened", "drive")
        return vc
    }

    func updateUIViewController(_ vc: UIDocumentPickerViewController, context: Context) {}

    final class Coordinator: NSObject, UIDocumentPickerDelegate {
        let onPick: (URL) -> Void
        let onCancel: () -> Void

        init(onPick: @escaping (URL) -> Void, onCancel: @escaping () -> Void) {
            self.onPick = onPick
            self.onCancel = onCancel
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            Log.write("folder picker: picked \(urls.map(\.path))", "drive")
            if let url = urls.first { onPick(url) } else { onCancel() }
        }

        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            Log.write("folder picker: cancelled", "drive")
            onCancel()
        }
    }
}

extension View {
    /// Present the folder picker and link what is chosen as the Drive folder.
    func linkFolderPicker(isPresented: Binding<Bool>, store: PackStore) -> some View {
        sheet(isPresented: isPresented) {
            FolderPicker(onPick: { url in
                isPresented.wrappedValue = false
                store.linkFolder(url)
                Task { await store.sync() }
            }, onCancel: {
                isPresented.wrappedValue = false
            })
            .ignoresSafeArea()
        }
    }
}
