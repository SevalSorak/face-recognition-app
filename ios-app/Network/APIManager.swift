import UIKit

class APIManager {
    static func recognizeFace(image: UIImage, completion: @escaping (Result<[String: Any], Error>) -> Void) {
        guard let url = URL(string: "http://localhost:5050/recognize-face") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        let imageData = image.jpegData(compressionQuality: 0.8)!
        var body = Data()

        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"face.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("❌ Hata:", error.localizedDescription)
                completion(.failure(error))
                return
            }

            guard let data = data else {
                print("❌ Veri boş geldi")
                completion(.failure(NSError(domain: "", code: -1)))
                return
            }

            // 🔍 JSON dönüşümünü test et
            do {
                if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("✅ Gelen JSON:", json)
                    completion(.success(json))
                } else {
                    print("❌ JSON dönüşüm başarısız")
                    completion(.failure(NSError(domain: "", code: -2)))
                }
            } catch {
                print("❌ JSON parsing hatası:", error.localizedDescription)
                completion(.failure(error))
            }
        }.resume()
    }
}
