import cv2
import os
import time
from mtcnn import MTCNN
import unicodedata

# Yüz verilerini kaydedeceğiniz dizin
def create_output_dir(output_dir="face_data"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# Yüz verilerini kaydetme fonksiyonu
def collect_face_data(name, surname, user_id, output_dir="face_data", directions=None, frames_per_direction=20):
    if directions is None:
        directions = ["Önden", "Sağ", "Sol"]  # Varsayılan yönler

    # MTCNN yüz algılama modeli
    detector = MTCNN()

    # Kamerayı aç
    cap = cv2.VideoCapture(0)

    user_folder_name = f"{user_id}_{name}_{surname}".replace(" ", "_")
    user_folder_path = os.path.join(output_dir, user_folder_name)
    os.makedirs(user_folder_path, exist_ok=True)

    direction_counter = 0  # yön geçişi
    # Yönler sırasıyla: Önden -> Sağ -> Sol
    while direction_counter < len(directions):
        print(f"Lütfen yüzünüzü {directions[direction_counter]} çevirin.")
        face_saved_count = 0  # Sadece kaydedilen yüz sayısı
        face_detected_once = False

        while face_saved_count < frames_per_direction:
            ret, frame = cap.read()
            if not ret:
                print("Kamera açılamadı.")
                break

            # Yüzleri algılamak için MTCNN kullanma
            results = detector.detect_faces(
                frame,
                min_face_size=15,  # Daha küçük yüzleri algıla
                threshold_pnet=0.5,  # PNet'ten daha fazla öneri
                threshold_rnet=0.6,  # RNet filtrelemesini gevşet
                threshold_onet=0.7   # ONet'ten daha fazla yüz kabul et
            )

            if results:
                face_detected_once = True
                for result in results:
                    x, y, w, h = result['box']
                    x, y = max(0, x), max(0, y)
                    face_image = frame[y:y+h, x:x+w]

                    if face_image.size == 0 or face_image.shape[0] < 50 or face_image.shape[1] < 50:
                        continue

                    timestamp = time.time()
                    timestamp_ms = int((timestamp % 1) * 1000)
                    normalized_name = unicodedata.normalize('NFKD', f"{name}_{surname}_{user_id}_{int(timestamp)}_{timestamp_ms}").encode('ASCII', 'ignore').decode('ASCII')
                    img_name = os.path.join(user_folder_path, f"{normalized_name}.jpg")
                    cv2.imwrite(img_name, face_image)
                    print(f"Yüz verisi kaydedildi: {img_name}")
                    face_saved_count += 1

                    # Görselde dikdörtgen çiz (kare ekranda görülsün)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            else:
                print("⚠️ Yüz algılanmadı, tekrar deneyin.")

            cv2.imshow(f"Yüz Algılama - {directions[direction_counter]}", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f"{directions[direction_counter]} yönü tamamlandı.")
        direction_counter += 1

    # Kamera kapanması
    cap.release()
    cv2.destroyAllWindows()
