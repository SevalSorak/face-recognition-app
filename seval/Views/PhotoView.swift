import SwiftUI

struct PhotoView: View {
    let imageData: Data?
    let confidence: Double

    var body: some View {
        VStack {
            Text("Tanıma Sonucu")
                .font(.title)
                .padding()
            
            if let imageData = imageData, let uiImage = UIImage(data: imageData) {
                Image(uiImage: uiImage)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 300, height: 300)
                    .background(Color.gray.opacity(0.2))
                    .cornerRadius(20)
                    .shadow(radius: 5)
                    .padding()
                
                VStack {
                    Text("Doğruluk Oranı")
                        .fontWeight(.bold)
                    
                    ConfidenceBar(value: confidence)
                        .frame(height: 30)
                        .padding(.horizontal)
                    
                    Text("\(Int(confidence * 100))%")
                        .font(.title)
                        .fontWeight(.bold)
                        .foregroundColor(confidenceColor(confidence))
                }
                .padding()
                .background(Color(UIColor.systemGray6))
                .cornerRadius(15)
                .padding()
                
                Spacer()
                
                Button(action: {
                    // Yeniden tarama işlemi
                }) {
                    Text("Yeniden Tara")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding(.bottom)
            } else {
                ZStack {
                    Rectangle()
                        .fill(Color.gray.opacity(0.2))
                        .frame(width: 300, height: 300)
                        .cornerRadius(20)
                    
                    Image(systemName: "person.fill")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: 150, height: 150)
                        .foregroundColor(.gray)
                }
                .padding()
                
                Text("Fotoğraf Yok")
                    .font(.headline)
                    .foregroundColor(.gray)
                
                Spacer()
                
                Button(action: {
                    // Fotoğraf çekme işlemi
                }) {
                    Text("Fotoğraf Çek")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding(.bottom)
            }
        }
        .frame(maxWidth: .infinity)
        .background(Color(UIColor.systemBackground))
    }

    private func confidenceColor(_ value: Double) -> Color {
        switch value {
        case 0..<0.5: return .red
        case 0.5..<0.7: return .orange
        case 0.7..<0.9: return .blue
        default: return .green
        }
    }
}
