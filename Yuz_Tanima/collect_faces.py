import cv2
import os
import time
from mtcnn import MTCNN

# Yüz verilerini kaydedeceğiniz dizin
def create_output_dir(output_dir="face_data"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# Yüz verilerini kaydetme fonksiyonu
def collect_face_data(name, surname, user_id, output_dir="face_data", directions=None, frames_per_direction=10):
    if directions is None:
        directions = ["Önden", "Sağ", "Sol"]  # Varsayılan yönler

    # MTCNN yüz algılama modeli
    detector = MTCNN()

    # Kamerayı aç
    cap = cv2.VideoCapture(0)

    # Yüz verilerini kaydetmek için sayaç
    img_counter = 0
    direction_counter = 0  # Yön sayacı

    # Yönler sırasıyla: Önden -> Sağ -> Sol
    while direction_counter < len(directions):
        print(f"Lütfen yüzünüzü {directions[direction_counter]} çevirin.")
        frame_counter = 0  # her bir yön için kare sayacı
        face_detected = False  # Yüz algılanıp algılanmadığını kontrol et

        while frame_counter < frames_per_direction:  # Her yön için kare sayısı kadar veri alıyoruz
            ret, frame = cap.read()
            if not ret:
                print("Kamera açılmadı.")
                break

            # Yüzleri algılamak için MTCNN kullanma
            results = detector.detect_faces(frame)

            # Eğer yüz algılandıysa
            if len(results) > 0:
                face_detected = True
                for result in results:
                    # Yüzün konumunu belirleyelim
                    (x, y, w, h) = result['box']

                    # Yüzü etrafında dikdörtgen çizme
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Yüz verisini kaydetme
                    face_image = frame[y:y + h, x:x + w]
                    timestamp = time.time()  # Şu anki zaman damgası
                    timestamp_ms = int((timestamp % 1) * 1000)  # Milisaniye kısmını al
                    img_name = os.path.join(output_dir, f"{name}_{surname}_{user_id}_{int(timestamp)}_{timestamp_ms}.jpg")
                    cv2.imwrite(img_name, face_image)
                    print(f"Yüz verisi kaydedildi: {img_name}")
                    img_counter += 1

            # Görüntüyü ekranda gösterme
            cv2.imshow(f"Face Detection - {directions[direction_counter]}", frame)

            # Kare sayacını arttır
            frame_counter += 1

            # 'q' tuşuna basarak çıkış yapma
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if not face_detected:
            print(f"{directions[direction_counter]} yönü için yüz tespit edilemedi.")
        
        # Bir yön tamamlandı, diğerine geçiş için yön sayacını arttır
        print(f"{directions[direction_counter]} yönü tamamlandı.")
        direction_counter += 1  # Bir yön tamamlandıktan sonra diğerine geç

    # Kamera kapanması
    cap.release()
    cv2.destroyAllWindows()
