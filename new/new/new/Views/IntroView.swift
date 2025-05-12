import SwiftUI
import UIKit
struct IntroView: View {
    @State private var showCamera = false
    @State private var image: UIImage? = nil

    @EnvironmentObject var manager: FaceRecognitionManager

    // Kullanıcı bilgileri
    let userId = "1705"
    let name = "seval"
    let surname = "sorak"

    var body: some View {
        ZStack {
            if let capturedImage = image {
                Image(uiImage: capturedImage)
                    .resizable()
                    .scaledToFill()
                    .ignoresSafeArea()
            } else {
                Color.black.ignoresSafeArea()
                Text("Henüz fotoğraf çekilmedi")
                    .foregroundColor(.white)
                    .font(.title3)
            }

            VStack {
                Spacer()

                Button("Kamerayı Aç") {
                    showCamera = true
                }
                .font(.headline)
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(12)
                .padding(.bottom, 50)

                if manager.addFaceSuccess {
                    Text("✅ Yüz başarıyla eklendi!")
                        .foregroundColor(.green)
                }

                if let error = manager.errorMessage {
                    Text("❌ \(error)")
                        .foregroundColor(.red)
                }
            }
        }
        .sheet(isPresented: $showCamera) {
            ImagePicker(sourceType: .camera) { pickedImage in
                if let pickedImage = pickedImage {
                    self.image = pickedImage
                    manager.addFace(image: pickedImage, name: name, surname: surname, userId: userId)
                }
            }
        }
    }
}




struct ImagePicker: UIViewControllerRepresentable {
    var sourceType: UIImagePickerController.SourceType = .camera
    var onImagePicked: (UIImage?) -> Void

    func makeCoordinator() -> Coordinator {
        Coordinator(onImagePicked: onImagePicked)
    }

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        picker.sourceType = sourceType
        picker.allowsEditing = false
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    class Coordinator: NSObject, UINavigationControllerDelegate, UIImagePickerControllerDelegate {
        var onImagePicked: (UIImage?) -> Void

        init(onImagePicked: @escaping (UIImage?) -> Void) {
            self.onImagePicked = onImagePicked
        }

        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            let image = info[.originalImage] as? UIImage
            onImagePicked(image)
            picker.dismiss(animated: true)
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            onImagePicked(nil)
            picker.dismiss(animated: true)
        }
    }
}
