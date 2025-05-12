import Foundation
import UIKit

// /recognize-face için model
struct FaceRecognitionResult: Codable {
    struct Result: Codable {
        let confidence: Double
        let label: Int
        let name: String
    }

    let results: [Result]?
    let status: String?
    let error: String?
}

// /add-face için model
struct AddFaceResponse: Codable {
    let message: String?
    let status: String?
    let error: String?
}

class FaceRecognitionManager: ObservableObject {
    @Published var recognitionResult: FaceRecognitionResult.Result?
    @Published var addFaceSuccess: Bool = false
    @Published var errorMessage: String?

    private let baseURL = "https://88b0-159-146-84-133.ngrok-free.app"

    func addFace(image: UIImage, name: String, surname: String, userId: String) {
        guard let url = URL(string: "\(baseURL)/add-face") else {
            self.errorMessage = "Geçersiz URL"
            return
        }

        let boundary = UUID().uuidString
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        let imageData = image.jpegData(compressionQuality: 0.8) ?? Data()
        let body = createMultipartBody(boundary: boundary, imageData: imageData, fields: [
            "name": name,
            "surname": surname,
            "user_id": userId
        ])

        request.httpBody = body

        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.errorMessage = "İstek hatası: \(error.localizedDescription)"
                    self.addFaceSuccess = false
                    return
                }

                guard let data = data else {
                    self.errorMessage = "Sunucudan veri gelmedi"
                    self.addFaceSuccess = false
                    return
                }

                do {
                    let result = try JSONDecoder().decode(AddFaceResponse.self, from: data)
                    if result.status == "success" {
                        self.addFaceSuccess = true
                        self.errorMessage = nil
                    } else {
                        self.addFaceSuccess = false
                        self.errorMessage = result.error ?? "Bilinmeyen hata"
                    }
                } catch {
                    self.errorMessage = "Yanıt çözümlenemedi: \(error.localizedDescription)"
                    self.addFaceSuccess = false
                }
            }
        }.resume()
    }

    func recognizeFace(image: UIImage) {
        guard let url = URL(string: "\(baseURL)/recognize-face") else {
            self.errorMessage = "Geçersiz URL"
            return
        }

        let boundary = UUID().uuidString
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        let imageData = image.jpegData(compressionQuality: 0.8) ?? Data()
        let body = createMultipartBody(boundary: boundary, imageData: imageData, fields: [:])

        request.httpBody = body

        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.errorMessage = "İstek hatası: \(error.localizedDescription)"
                    return
                }

                guard let data = data else {
                    self.errorMessage = "Sunucudan veri gelmedi"
                    return
                }

                do {
                    let result = try JSONDecoder().decode(FaceRecognitionResult.self, from: data)
                    if let first = result.results?.first {
                        self.recognitionResult = first
                        self.errorMessage = nil
                    } else {
                        self.errorMessage = "Tanıma sonucu alınamadı"
                    }
                } catch {
                    self.errorMessage = "Yanıt çözümlenemedi: \(error.localizedDescription)"
                }
            }
        }.resume()
    }

    private func createMultipartBody(boundary: String, imageData: Data, fields: [String: String]) -> Data {
        var body = Data()
        let lineBreak = "\r\n"

        for (key, value) in fields {
            body.append("--\(boundary)\(lineBreak)")
            body.append("Content-Disposition: form-data; name=\"\(key)\"\(lineBreak)\(lineBreak)")
            body.append("\(value)\(lineBreak)")
        }

        body.append("--\(boundary)\(lineBreak)")
        body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\(lineBreak)")
        body.append("Content-Type: image/jpeg\(lineBreak)\(lineBreak)")
        body.append(imageData)
        body.append(lineBreak)
        body.append("--\(boundary)--\(lineBreak)")

        return body
    }
}

extension Data {
    mutating func append(_ string: String) {
        if let data = string.data(using: .utf8) {
            append(data)
        }
    }
}
