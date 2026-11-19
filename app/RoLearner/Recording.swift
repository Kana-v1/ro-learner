import AVFoundation

/// The learner's recorded answers: one AAC file per attempt, in a folder per
/// session, so a miss can be listened to and the recognisers checked against
/// what was actually said.
enum Recording {
    static let dir: URL = {
        let support = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        return support.appendingPathComponent("Recordings", isDirectory: true)
    }()

    /// Sessions whose recordings stay on the phone once they're sent.
    static let keep = 10

    static func url(session: String, file: String) -> URL {
        dir.appendingPathComponent(session, isDirectory: true).appendingPathComponent(file)
    }

    /// Encode 16 kHz mono samples as AAC. Called off the main thread.
    static func write(_ samples: [Float], to url: URL) {
        guard !samples.isEmpty,
              let format = AVAudioFormat(commonFormat: .pcmFormatFloat32, sampleRate: 16_000,
                                         channels: 1, interleaved: false),
              let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: AVAudioFrameCount(samples.count)),
              let channel = buffer.floatChannelData?[0] else { return }
        buffer.frameLength = AVAudioFrameCount(samples.count)
        samples.withUnsafeBufferPointer { channel.update(from: $0.baseAddress!, count: samples.count) }
        let settings: [String: Any] = [AVFormatIDKey: kAudioFormatMPEG4AAC,
                                       AVSampleRateKey: 16_000,
                                       AVNumberOfChannelsKey: 1]
        do {
            try FileManager.default.createDirectory(at: url.deletingLastPathComponent(),
                                                    withIntermediateDirectories: true)
            // The file is finalised when it goes out of scope.
            let file = try AVAudioFile(forWriting: url, settings: settings,
                                       commonFormat: .pcmFormatFloat32, interleaved: false)
            try file.write(from: buffer)
        } catch {
            Log.write("saving \(url.lastPathComponent) failed: \(error)", "audio")
        }
    }

    /// Delete the recordings of all but the newest `keep` sessions, never one
    /// still waiting to be sent.
    static func prune(unsent: Set<String>) {
        let fm = FileManager.default
        let folders = (try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: [.contentModificationDateKey])) ?? []
        let byAge = folders.sorted {
            let a = (try? $0.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
            let b = (try? $1.resourceValues(forKeys: [.contentModificationDateKey]).contentModificationDate) ?? .distantPast
            return a > b
        }
        for f in byAge.dropFirst(keep) where !unsent.contains(f.lastPathComponent) {
            try? fm.removeItem(at: f)
        }
    }
}

/// Plays one recorded answer in the results.
@MainActor
final class RecordingPlayer: ObservableObject {
    @Published private(set) var playing: URL?
    private var player: AVAudioPlayer?

    func toggle(_ url: URL) {
        if playing == url { stop(); return }
        stop()
        do {
            // An episode left open in the mini-player keeps the mic's
            // category; switching it here would break that session.
            let audio = AVAudioSession.sharedInstance()
            if audio.category != .playAndRecord {
                try audio.setCategory(.playback, mode: .default)
                try audio.setActive(true)
            }
            let p = try AVAudioPlayer(contentsOf: url)
            p.play()
            player = p
            playing = url
            let length = p.duration
            Task { [weak self] in
                try? await Task.sleep(nanoseconds: UInt64((length + 0.2) * 1_000_000_000))
                if self?.playing == url { self?.stop() }
            }
        } catch {
            Log.write("playing \(url.lastPathComponent) failed: \(error)", "audio")
        }
    }

    func stop() {
        player?.stop()
        player = nil
        playing = nil
    }
}
