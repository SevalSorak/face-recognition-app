import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = RecognitionViewModel()
    @StateObject private var manager = FaceRecognitionManager()

    @State private var isIntroFinished = false

    var body: some View {
        if !isIntroFinished {
            // 🔰 İlk girişte yönlendirme ekranı
            IntroView()
                .environmentObject(manager)
        } else {
            if viewModel.recognizedPerson != nil {
                // ✅ Tanıma başarılıysa: Detay ekranı
                recognizedDetailScreen
            } else {
                // ❌ Tanıma yapılmadıysa: Basit ekran
                simpleIntroScreen
            }
        }
    }

    var recognizedDetailScreen: some View {
        VStack(spacing: 0) {
            HStack(spacing: 0) {
                PersonalInfoView(person: viewModel.recognizedPerson)
                PhotoView(imageData: viewModel.currentFaceImage, confidence: viewModel.recognitionConfidence)
            }
            .frame(height: UIScreen.main.bounds.height * 0.6)

            VStack {
                VoiceRecognitionView(isRecording: $viewModel.isRecording)
                ChatView(
                    messages: viewModel.messages,
                    newMessage: $viewModel.newMessage,
                    sendAction: viewModel.sendMessage
                )
            }
            .frame(height: UIScreen.main.bounds.height * 0.4)
            .background(Color(UIColor.systemGray6))
        }
        .edgesIgnoringSafeArea(.all)
    }

    var simpleIntroScreen: some View {
        VStack(spacing: 30) {
            Text("Yüz Tanıma Başlatılmadı")
                .font(.title)
                .padding(.top, 50)

            Button("Tanımaya Başla") {
                // Örnek verilerle tanıma simülasyonu
                viewModel.recognizedPerson = Person(
                    id: "1",
                    firstName: "Test",
                    lastName: "Kişisi",
                    age: 30,
                    gender: "Kadın",
                    occupation: "Mühendis",
                    phoneNumber: "0000000000",
                    email: "test@example.com"
                )
                viewModel.recognitionConfidence = 0.85
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(12)
        }
    }
}
