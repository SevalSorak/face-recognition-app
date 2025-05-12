import Foundation

// Chat mesaj modeli
struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isFromUser: Bool
    let timestamp: Date = Date()
}
