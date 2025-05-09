import AVFoundation
import UIKit

class PhotoCaptureDelegate: NSObject, AVCapturePhotoCaptureDelegate {
    private let completion: (UIImage?) -> Void

    init(completion: @escaping (UIImage?) -> Void) {
        self.completion = completion
    }

    func photoOutput(_ output: AVCapturePhotoOutput,
                     didFinishProcessingPhoto photo: AVCapturePhoto,
                     error: Error?) {
        if let error = error {
            print("📸 Fotoğraf çekme hatası: \(error.localizedDescription)")
            completion(nil)
            return
        }

        guard let data = photo.fileDataRepresentation(),
              let image = UIImage(data: data) else {
            print("⚠️ Fotoğraf verisi alınamadı veya UIImage oluşturulamadı.")
            completion(nil)
            return
        }

        print("✅ Fotoğraf başarıyla çekildi.")
        completion(image)
    }
}
