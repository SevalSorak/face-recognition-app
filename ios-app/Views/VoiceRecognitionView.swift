import SwiftUI

struct VoiceRecognitionView: View {
    @Binding var isRecording: Bool
    @State private var animationAmount: CGFloat = 1

    var body: some View {
        VStack {
            Text("Ses Tanıma")
                .font(.title2)
                .padding(.top)
            
            ZStack {
                Circle()
                    .stroke(isRecording ? Color.red : Color.blue, lineWidth: 3)
                    .scaleEffect(isRecording ? animationAmount : 1)
                    .opacity(isRecording ? Double(2 - animationAmount) : 1)
                    .animation(
                        isRecording ?
                            Animation.easeOut(duration: 1).repeatForever(autoreverses: false)
                            : .default,
                        value: animationAmount
                    )
                
                Circle()
                    .fill(isRecording ? Color.red : Color.blue)
                    .frame(width: 80, height: 80)
                    .overlay(
                        Image(systemName: "mic.fill")
                            .font(.system(size: 40))
                            .foregroundColor(.white)
                    )
                    .onTapGesture {
                        isRecording.toggle()
                        if isRecording {
                            animationAmount = 2
                        }
                    }
            }
            .frame(width: 100, height: 100)
            .padding()
            
            Text(isRecording ? "Dinleniyor..." : "Konuşmak için dokun")
                .foregroundColor(isRecording ? .red : .blue)
                .padding(.bottom)
        }
    }
}
