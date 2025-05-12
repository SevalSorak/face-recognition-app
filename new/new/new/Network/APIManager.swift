import UIKit

class APIManager {
    static func recognizeFace(image: UIImage, completion: @escaping (Result<[String: Any], Error>) -> Void) {
        // API URL'sini .env'den almalısınız
        guard let url = URL(string: "https://88b0-159-146-84-133.ngrok-free.app/recognize-face") else {
            print("❌ Geçersiz URL")
            completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Geçersiz URL"])))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.timeoutInterval = 30 // 30 saniye timeout

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            print("❌ Görüntü veriye dönüştürülemedi")
            completion(.failure(NSError(domain: "", code: -2, userInfo: [NSLocalizedDescriptionKey: "Görüntü veriye dönüştürülemedi"])))
            return
        }

        var body = Data()

        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"face.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        print("📤 API isteği gönderiliyor...")
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("❌ Ağ hatası:", error.localizedDescription)
                completion(.failure(error))
                return
            }

            if let httpResponse = response as? HTTPURLResponse {
                print("📥 HTTP Durum Kodu:", httpResponse.statusCode)
                
                if !(200...299).contains(httpResponse.statusCode) {
                    print("❌ Sunucu hatası:", httpResponse.statusCode)
                    completion(.failure(NSError(domain: "", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Sunucu hatası: \(httpResponse.statusCode)"])))
                    return
                }
            }

            guard let data = data else {
                print("❌ Veri boş geldi")
                completion(.failure(NSError(domain: "", code: -3, userInfo: [NSLocalizedDescriptionKey: "Sunucudan veri alınamadı"])))
                return
            }

            // Gelen veriyi string olarak yazdır (debug için)
            if let responseString = String(data: data, encoding: .utf8) {
                print("📦 Ham yanıt:", responseString)
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("✅ JSON başarıyla ayrıştırıldı:", json)
                    completion(.success(json))
                } else {
                    print("❌ JSON formatı geçersiz")
                    completion(.failure(NSError(domain: "", code: -4, userInfo: [NSLocalizedDescriptionKey: "Geçersiz JSON formatı"])))
                }
            } catch {
                print("❌ JSON ayrıştırma hatası:", error.localizedDescription)
                completion(.failure(error))
            }
        }.resume()
    }
}
