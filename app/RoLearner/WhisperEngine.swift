import Foundation
import WhisperKit

/// Whisper on the phone (Settings → Recognition → Whisper), through WhisperKit.
///
/// Apple's recogniser can't be told what to expect in Romanian — iOS has no
/// Romanian data for its custom language models — so it guesses among all of
/// Romanian, and short or similar-sounding words come back wrong ("Puiul meu"
/// for "Fiul meu", nothing for "mic"). Whisper is an open model (OpenAI, MIT
/// licence) that runs entirely on the phone and takes a text prompt: each
/// answer is transcribed with the drill's expected answer as the prompt, which
/// steers it toward the course's words without forcing them.
///
/// Apple's recogniser keeps running alongside to decide when the learner has
/// finished; Whisper transcribes the recorded answer at that moment. Both
/// transcripts are kept with every attempt, so the two can be compared from
/// the results.
///
/// The model (large-v3, the 2024-09-30 release, compressed to 626 MB) is
/// downloaded once, on request, into Application Support (not backed up to
/// iCloud). The first load compiles it for the phone's Neural Engine, which
/// takes a few minutes; later loads take seconds.
@MainActor
final class WhisperEngine: ObservableObject {
    static let shared = WhisperEngine()
    static let variant = "large-v3-v20240930_626MB"

    enum State: Equatable {
        case notDownloaded
        case downloading(Double)      // 0...1
        case loading                  // first time: compiling for the Neural Engine
        case ready
        case failed(String)
    }

    @Published private(set) var state: State = .notDownloaded
    private var pipe: WhisperKit?

    private let base: URL = {
        var url = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("Whisper", isDirectory: true)
        try? FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
        var values = URLResourceValues()
        values.isExcludedFromBackup = true
        try? url.setResourceValues(values)
        return url
    }()

    private var savedFolder: URL? {
        get { UserDefaults.standard.string(forKey: "whisperFolder").map { URL(fileURLWithPath: $0) } }
        set { UserDefaults.standard.set(newValue?.path, forKey: "whisperFolder") }
    }

    var isReady: Bool { state == .ready }

    var statusText: String {
        switch state {
        case .notDownloaded: return "not downloaded"
        case .downloading(let p): return "downloading, \(Int(p * 100))%"
        case .loading: return "preparing — the first time takes a few minutes"
        case .ready: return "ready"
        case .failed(let why): return "failed: \(why)"
        }
    }

    /// At launch: load the model if it was downloaded before.
    func loadIfDownloaded() {
        guard state == .notDownloaded, let folder = savedFolder,
              FileManager.default.fileExists(atPath: folder.path) else { return }
        Task { await load(folder) }
    }

    /// Settings → Download: fetch the model, then load it.
    func download() {
        switch state {
        case .downloading, .loading, .ready: return
        default: break
        }
        state = .downloading(0)
        Log.write("whisper: downloading \(Self.variant)", "speech")
        Task {
            do {
                let folder = try await WhisperKit.download(variant: Self.variant, downloadBase: base) { progress in
                    let fraction = progress.fractionCompleted
                    Task { @MainActor in
                        if case .downloading = WhisperEngine.shared.state {
                            WhisperEngine.shared.state = .downloading(fraction)
                        }
                    }
                }
                savedFolder = folder
                Log.write("whisper: downloaded to \(folder.lastPathComponent)", "speech")
                await load(folder)
            } catch {
                state = .failed(error.localizedDescription)
                Log.write("whisper: download failed: \(error)", "speech")
            }
        }
    }

    private func load(_ folder: URL) async {
        state = .loading
        let started = Date()
        do {
            // The tokenizer is fetched on the first load; kept next to the model
            // so later loads work offline.
            let config = WhisperKitConfig(modelFolder: folder.path, tokenizerFolder: base,
                                          verbose: false, logLevel: .error,
                                          prewarm: true, load: true, download: false)
            pipe = try await WhisperKit(config)
            state = .ready
            Log.write("whisper: ready in \(String(format: "%.0f", Date().timeIntervalSince(started))) s", "speech")
        } catch {
            pipe = nil
            state = .failed(error.localizedDescription)
            Log.write("whisper: load failed: \(error)", "speech")
        }
    }

    /// Transcribe one answer (16 kHz mono). `prompt` is the drill's expected
    /// answer and its accepted phrasings: Whisper reads it as the text that
    /// came just before, which makes those words likely without forcing them.
    func transcribe(_ audio: [Float], prompt: String) async -> String? {
        guard let pipe, !audio.isEmpty else { return nil }
        var options = DecodingOptions()
        options.language = "ro"
        options.detectLanguage = false
        options.temperature = 0
        options.temperatureFallbackCount = 2
        options.usePrefillPrompt = true
        options.skipSpecialTokens = true
        options.withoutTimestamps = true
        if let tokenizer = pipe.tokenizer {
            let begin = tokenizer.specialTokens.specialTokenBegin
            options.promptTokens = tokenizer.encode(text: " " + prompt).filter { $0 < begin }
        }
        do {
            let results = try await pipe.transcribe(audioArray: audio, decodeOptions: options)
            let text = results.map(\.text).joined(separator: " ")
                .trimmingCharacters(in: .whitespacesAndNewlines)
            return text.isEmpty ? nil : text
        } catch {
            Log.write("whisper: transcribe failed: \(error)", "speech")
            return nil
        }
    }
}
