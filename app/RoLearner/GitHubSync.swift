import Foundation
import Security

/// The GitHub token lives in the Keychain, never in the app's files.
enum Keychain {
    private static let service = "vorbeste"

    static func get(_ account: String) -> String? {
        let q: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrService as String: service,
                                kSecAttrAccount as String: account,
                                kSecReturnData as String: true,
                                kSecMatchLimit as String: kSecMatchLimitOne]
        var out: AnyObject?
        guard SecItemCopyMatching(q as CFDictionary, &out) == errSecSuccess,
              let data = out as? Data else { return nil }
        return String(data: data, encoding: .utf8)
    }

    static func set(_ value: String?, for account: String) {
        let base: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                   kSecAttrService as String: service,
                                   kSecAttrAccount as String: account]
        SecItemDelete(base as CFDictionary)
        guard let value else { return }
        var add = base
        add[kSecValueData as String] = Data(value.utf8)
        add[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlock
        SecItemAdd(add as CFDictionary, nil)
    }
}

/// Sync through a private GitHub repository (see its README): episodes come
/// from the release "episodes", results and the log go to results/ and logs/,
/// Claude's notes come from notes/. Plain HTTPS to GitHub, so unlike iCloud it
/// happens now, not whenever iCloud gets round to it.
enum GitHubSync {
    /// Asset downloads redirect from api.github.com to a storage host that
    /// rejects a request still carrying the GitHub token — drop it there.
    private final class DropAuthOnRedirect: NSObject, URLSessionTaskDelegate, @unchecked Sendable {
        func urlSession(_ session: URLSession, task: URLSessionTask,
                        willPerformHTTPRedirection response: HTTPURLResponse,
                        newRequest request: URLRequest,
                        completionHandler: @escaping (URLRequest?) -> Void) {
            var r = request
            if r.url?.host != "api.github.com" { r.setValue(nil, forHTTPHeaderField: "Authorization") }
            completionHandler(r)
        }
    }

    private static let session = URLSession(configuration: .default, delegate: DropAuthOnRedirect(),
                                            delegateQueue: nil)

    struct Failure: Error, LocalizedError {
        let message: String
        var errorDescription: String? { message }
    }

    private static func request(_ path: String, token: String, method: String = "GET",
                                body: [String: Any]? = nil, accept: String = "application/vnd.github+json") -> URLRequest {
        var r = URLRequest(url: URL(string: "https://api.github.com" + path)!)
        r.httpMethod = method
        r.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        r.setValue(accept, forHTTPHeaderField: "Accept")
        r.setValue("2022-11-28", forHTTPHeaderField: "X-GitHub-Api-Version")
        r.setValue("Vorbeste", forHTTPHeaderField: "User-Agent")
        if let body {
            r.httpBody = try? JSONSerialization.data(withJSONObject: body)
            r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        }
        r.timeoutInterval = 60
        return r
    }

    private static func json(_ r: URLRequest) async throws -> (Any?, Int) {
        let (data, response) = try await session.data(for: r)
        let code = (response as? HTTPURLResponse)?.statusCode ?? 0
        return (try? JSONSerialization.jsonObject(with: data), code)
    }

    private static func date(_ s: Any?) -> Date {
        (s as? String).flatMap { ISO8601DateFormatter().date(from: $0) } ?? .distantPast
    }

    /// Quick check for the Settings screen: can this token see this repo?
    static func check(repo: String, token: String) async -> String? {
        do {
            let (obj, code) = try await json(request("/repos/\(repo)", token: token))
            if code == 200 { return nil }
            let msg = (obj as? [String: Any])?["message"] as? String ?? "HTTP \(code)"
            return "GitHub says: \(msg)"
        } catch {
            return error.localizedDescription
        }
    }

    static func run(repo: String, token: String, known: [String: Date], haveSlugs: Set<String>,
                    outgoing: [DriveSync.Outgoing], log: Data?) async -> (DriveSync.Outcome, [String: Date]) {
        var outcome = DriveSync.Outcome()
        var baseline: [String: Date] = [:]      // assets we already have from iCloud: remember, don't download
        let tmp = FileManager.default.temporaryDirectory.appendingPathComponent("gh-pull", isDirectory: true)
        try? FileManager.default.createDirectory(at: tmp, withIntermediateDirectories: true)
        Log.write("sync with GitHub \(repo)", "sync")

        // episodes: the release's assets, new or updated ones only
        do {
            let (obj, code) = try await json(request("/repos/\(repo)/releases/tags/episodes", token: token))
            if code == 404 {
                Log.write("no 'episodes' release yet", "sync")
            } else if code != 200 {
                outcome.problem = "Episodes: HTTP \(code)"
                Log.write("episodes list failed: HTTP \(code) \(obj ?? "")", "sync")
            } else {
                let assets = (obj as? [String: Any])?["assets"] as? [[String: Any]] ?? []
                for a in assets {
                    guard let name = a["name"] as? String, name.hasSuffix(".rolesson"),
                          let url = a["url"] as? String else { continue }
                    let key = "gh:episodes/\(name)"
                    let updated = date(a["updated_at"])
                    if let seen = known[key], seen >= updated { continue }
                    let slug = name.replacingOccurrences(of: "episode_", with: "")
                        .replacingOccurrences(of: ".rolesson", with: "")
                    if known[key] == nil && haveSlugs.contains(slug) {
                        baseline[key] = updated
                        continue
                    }
                    var r = request("", token: token, accept: "application/octet-stream")
                    r.url = URL(string: url)
                    let (file, response) = try await session.download(for: r)
                    let status = (response as? HTTPURLResponse)?.statusCode ?? 0
                    guard status == 200 else {
                        outcome.problem = "Download \(name): HTTP \(status)"
                        Log.write("download \(name) failed: HTTP \(status)", "sync")
                        continue
                    }
                    let dest = tmp.appendingPathComponent(name)
                    try? FileManager.default.removeItem(at: dest)
                    try FileManager.default.moveItem(at: file, to: dest)
                    outcome.lessons.append(DriveSync.Pulled(name: key, modified: updated, local: dest))
                    Log.write("downloaded \(name)", "sync")
                }
            }
        } catch {
            outcome.problem = error.localizedDescription
            Log.write("episodes failed: \(error)", "sync")
        }

        // Claude's notes
        do {
            let (obj, code) = try await json(request("/repos/\(repo)/contents/notes", token: token))
            if code == 200, let items = obj as? [[String: Any]] {
                for item in items {
                    guard let name = item["name"] as? String, name.hasSuffix(".roanalysis") else { continue }
                    let key = "gh:notes/\(name)"
                    if known[key] != nil { continue }
                    let (file, fcode) = try await json(request("/repos/\(repo)/contents/notes/\(name)", token: token))
                    guard fcode == 200, let b64 = (file as? [String: Any])?["content"] as? String,
                          let data = Data(base64Encoded: b64, options: .ignoreUnknownCharacters) else { continue }
                    let dest = tmp.appendingPathComponent(name)
                    try data.write(to: dest)
                    outcome.notes.append(DriveSync.Pulled(name: key, modified: Date(), local: dest))
                    Log.write("downloaded note \(name)", "sync")
                }
            }
        } catch {
            Log.write("notes failed: \(error)", "sync")
        }

        // results, then the log
        for o in outgoing {
            if await put(repo: repo, token: token, path: "\(o.folder)/\(o.fileName)", data: o.data,
                         message: o.folder == "feedback" ? "Feedback \(o.key)" : "Result \(o.key)") {
                outcome.pushed.append(o.key)
            } else {
                outcome.problem = "Couldn't upload \(o.fileName)"
            }
        }
        if let log {
            _ = await put(repo: repo, token: token, path: "logs/vorbeste-log.txt",
                          data: Data(log.suffix(300_000)), message: "Log")
        }
        return (outcome, baseline)
    }

    /// Create or replace a file through the contents API.
    private static func put(repo: String, token: String, path: String, data: Data, message: String) async -> Bool {
        do {
            var sha: String?
            let (existing, code) = try await json(request("/repos/\(repo)/contents/\(path)", token: token))
            if code == 200 { sha = (existing as? [String: Any])?["sha"] as? String }
            var body: [String: Any] = ["message": message, "content": data.base64EncodedString()]
            if let sha { body["sha"] = sha }
            let (obj, putCode) = try await json(request("/repos/\(repo)/contents/\(path)", token: token,
                                                        method: "PUT", body: body))
            if putCode == 200 || putCode == 201 {
                Log.write("uploaded \(path)", "sync")
                return true
            }
            Log.write("upload \(path) failed: HTTP \(putCode) \((obj as? [String: Any])?["message"] ?? "")", "sync")
        } catch {
            Log.write("upload \(path) failed: \(error)", "sync")
        }
        return false
    }
}
