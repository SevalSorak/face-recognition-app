import Foundation
import AVFoundation
import SwiftUI

class RecognitionViewModel: ObservableObject {
    @Published var recognizedPerson: Person?
    @Published var currentFaceImage: Data?
    @Published var recognitionConfidence: Double = 0.0
    @Published var isRecording: Bool = false
    @Published var messages: [ChatMessage] = []
    @Published var newMessage: String = ""
    
    // Örnek veriler
    init() {
        // Örnek kişi
        recognizedPerson = Person(
            id: "1",
            firstName: "Ahmet",
            lastName: "Yılmaz",
            age: 32,
            gender: "Erkek",
            occupation: "Mühendis",
            phoneNumber: "+90 555 123 4567",
            email: "ahmet.yilmaz@example.com"
        )
        
        // Örnek mesajlar
        messages = [
            ChatMessage(text: "Merhaba, size nasıl yardımcı olabilirim?", isFromUser: false),
            ChatMessage(text: "Merhaba, bugün toplantım var mı?", isFromUser: true),
            ChatMessage(text: "Evet, saat 14:00'de Proje Değerlendirme toplantınız var.", isFromUser: false)
        ]
        
        // Simüle edilmiş doğruluk oranı
        recognitionConfidence = 0.85
    }
    
    // Yeni mesaj gönderme işlemi
    func sendMessage() {
        guard !newMessage.isEmpty else { return }
        
        // Kullanıcı mesajını ekleme
        let userMessage = ChatMessage(text: newMessage, isFromUser: true)
        messages.append(userMessage)
        
        // Mesaj kutusunu temizleme
        newMessage = ""
        
        // Yapay yanıt
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            let botMessage = ChatMessage(text: "Anlaşıldı, yardımcı oluyorum.", isFromUser: false)
            self.messages.append(botMessage)
        }
    }
}
