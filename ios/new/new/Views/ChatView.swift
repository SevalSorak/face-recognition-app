import SwiftUI

struct ChatView: View {
    let messages: [ChatMessage]
    @Binding var newMessage: String
    let sendAction: () -> Void

    var body: some View {
        VStack {
            Text("Sohbet")
                .font(.title2)
                .padding(.top)
            
            ScrollView {
                LazyVStack {
                    ForEach(messages) { message in
                        ChatBubble(message: message)
                            .padding(.horizontal)
                    }
                }
                .padding(.vertical, 5)
            }
            
            HStack {
                TextField("Mesaj yazın...", text: $newMessage)
                    .padding(10)
                    .background(Color(UIColor.systemGray5))
                    .cornerRadius(20)
                
                Button(action: sendAction) {
                    Image(systemName: "paperplane.fill")
                        .font(.system(size: 22))
                        .foregroundColor(.blue)
                        .padding(10)
                }
                .disabled(newMessage.isEmpty)
            }
            .padding()
        }
    }
}
