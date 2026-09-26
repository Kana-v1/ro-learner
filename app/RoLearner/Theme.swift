import SwiftUI
import UIKit

/// The look from the design canvas: deep ink ground, warm ivory text, one amber
/// accent that always means "your turn" or "the thing to press", green for right
/// and orange for not quite (each always paired with an icon, never colour alone).
enum Theme {
    static let bg = Color(hex: 0x0E1116)
    static let surface = Color(hex: 0x171B22)
    static let raised = Color(hex: 0x1A1F27)
    static let chip = Color(hex: 0x232934)
    static let line = Color(hex: 0x2A313D)
    static let lineStrong = Color(hex: 0x3A4250)
    static let tick = Color(hex: 0x5A6372)
    static let text = Color(hex: 0xF3EFE6)
    static let text2 = Color(hex: 0xA9B0BC)
    static let muted = Color(hex: 0x8A93A1)
    static let accent = Color(hex: 0xF4B942)
    static let onAccent = Color(hex: 0x1A1406)
    static let right = Color(hex: 0x57D18C)
    static let onRight = Color(hex: 0x07170E)
    static let notQuite = Color(hex: 0xFF7A45)
    static let onNotQuite = Color(hex: 0x1F0C04)
    static let info = Color(hex: 0x7FB2FF)
    static let infoCard = Color(hex: 0x152033)
    static let infoLine = Color(hex: 0x27405F)

    /// Titles and the big status words. The system serif (New York) stands in for
    /// the canvas's Fraunces so no font files need bundling.
    static func display(_ size: CGFloat) -> Font {
        .system(size: size, weight: .semibold, design: .serif)
    }

    static let claudePhrase = "Read my Romanian results from Google Drive"
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255,
                  green: Double((hex >> 8) & 0xFF) / 255,
                  blue: Double(hex & 0xFF) / 255)
    }
}

extension Verdict {
    var title: String {
        switch self {
        case .correct: return "Right"
        case .close: return "Almost"
        case .missed: return "Not quite"
        case .noAnswer: return "Didn't catch that"
        case .unmarked: return ""
        }
    }

    var color: Color {
        switch self {
        case .correct: return Theme.right
        case .close, .missed, .noAnswer: return Theme.notQuite
        case .unmarked: return Theme.muted
        }
    }

    var ink: Color { self == .correct ? Theme.onRight : Theme.onNotQuite }
    var symbol: String { self == .correct ? "checkmark" : "xmark" }
}

func timeString(_ seconds: Double) -> String {
    let s = max(0, Int(seconds.rounded(.down)))
    return String(format: "%d:%02d", s / 60, s % 60)
}

// MARK: - building blocks

struct CardBox<Content: View>: View {
    var fill: Color = Theme.surface
    var stroke: Color = Theme.line
    @ViewBuilder var content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: 12) { content }
            .padding(16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(fill, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
            .overlay(RoundedRectangle(cornerRadius: 20, style: .continuous).stroke(stroke))
    }
}

struct SectionLabel: View {
    let text: String
    var color: Color = Theme.muted

    var body: some View {
        Text(text).font(.system(size: 12, weight: .bold)).tracking(1).foregroundStyle(color)
    }
}

struct AccentButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 16, weight: .semibold))
            .frame(maxWidth: .infinity, minHeight: 50)
            .foregroundStyle(Theme.onAccent)
            .background(Theme.accent.opacity(configuration.isPressed ? 0.8 : 1),
                        in: RoundedRectangle(cornerRadius: 14, style: .continuous))
    }
}

struct OutlineButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 15, weight: .medium))
            .frame(maxWidth: .infinity, minHeight: 48)
            .foregroundStyle(Theme.text)
            .background(configuration.isPressed ? Theme.chip : Color.clear,
                        in: RoundedRectangle(cornerRadius: 14, style: .continuous))
            .overlay(RoundedRectangle(cornerRadius: 14, style: .continuous).stroke(Theme.lineStrong))
    }
}

struct CircleIconButton: View {
    let symbol: String
    let label: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: symbol).font(.system(size: 17, weight: .semibold))
                .frame(width: 44, height: 44)
                .background(Theme.surface, in: Circle())
                .overlay(Circle().stroke(Theme.line))
        }
        .foregroundStyle(Theme.text)
        .accessibilityLabel(label)
    }
}

struct Pill: View {
    let text: String
    var symbol: String?
    let foreground: Color
    let background: Color

    var body: some View {
        HStack(spacing: 4) {
            if let symbol { Image(systemName: symbol).font(.system(size: 10, weight: .bold)) }
            Text(text).font(.system(size: 12, weight: .bold))
        }
        .padding(.horizontal, 9).padding(.vertical, 4)
        .foregroundStyle(foreground)
        .background(background, in: Capsule())
    }
}

/// The big round status mark in the player: amber mic, green check, orange cross.
struct StatusDisc: View {
    let color: Color
    let ink: Color
    let symbol: String

    var body: some View {
        Circle().stroke(color.opacity(0.35), lineWidth: 2)
            .frame(width: 168, height: 168)
            .overlay(
                Circle().fill(color).frame(width: 122, height: 122)
                    .overlay(Image(systemName: symbol).font(.system(size: 46, weight: .semibold)).foregroundStyle(ink))
            )
            .accessibilityHidden(true)
    }
}

struct NumberBadge: View {
    let number: Int
    var active = false
    var done = false

    var body: some View {
        ZStack {
            if active || done {
                Circle().fill(done ? Theme.right : Theme.accent)
            } else {
                Circle().stroke(Theme.lineStrong)
            }
            if done {
                Image(systemName: "checkmark").font(.system(size: 13, weight: .bold)).foregroundStyle(Theme.onRight)
            } else {
                Text("\(number)").font(.system(size: 14, weight: .bold))
                    .foregroundStyle(active ? Theme.onAccent : Theme.text)
            }
        }
        .frame(width: 30, height: 30)
    }
}

/// The phrase to say to Claude, with a copy button.
struct PhraseBox: View {
    @State private var copied = false

    var body: some View {
        HStack(spacing: 8) {
            Text("“\(Theme.claudePhrase)”").font(.system(size: 14)).foregroundStyle(Theme.text)
                .frame(maxWidth: .infinity, alignment: .leading)
            Button {
                UIPasteboard.general.string = Theme.claudePhrase
                copied = true
            } label: {
                Image(systemName: copied ? "checkmark" : "doc.on.doc").font(.system(size: 15, weight: .semibold))
                    .frame(width: 36, height: 36)
                    .background(Color(hex: 0x2F3744), in: RoundedRectangle(cornerRadius: 10))
            }
            .foregroundStyle(copied ? Theme.right : Theme.text)
            .accessibilityLabel(copied ? "Copied" : "Copy phrase")
        }
        .padding(.horizontal, 12).padding(.vertical, 10)
        .background(Theme.chip, in: RoundedRectangle(cornerRadius: 12))
    }
}

/// The iOS share sheet, reporting whether the user actually sent the file, so an
/// upload only counts once it happened.
struct ShareSheet: UIViewControllerRepresentable {
    let items: [Any]
    let onComplete: (Bool) -> Void

    func makeUIViewController(context: Context) -> UIActivityViewController {
        let vc = UIActivityViewController(activityItems: items, applicationActivities: nil)
        vc.completionWithItemsHandler = { _, completed, _, _ in onComplete(completed) }
        return vc
    }

    func updateUIViewController(_ vc: UIActivityViewController, context: Context) {}
}

struct ShareItem: Identifiable {
    let id = UUID()
    let url: URL
    let keys: [String]
}
