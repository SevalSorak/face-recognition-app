import SwiftUI

struct ConfidenceBar: View {
    let value: Double

    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                Rectangle()
                    .fill(Color.gray.opacity(0.3))
                    .cornerRadius(5)
                
                Rectangle()
                    .fill(confidenceColor(value))
                    .frame(width: CGFloat(value) * geometry.size.width)
                    .cornerRadius(5)
            }
        }
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
