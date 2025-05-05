import cv2
import numpy as np
import os
from mtcnn import MTCNN
detector = MTCNN()

# Model ve cascade yükleyici
def load_models():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trained_face_model.yml')
    return recognizer

# Dosya adından kullanıcı bilgilerini çıkarmak
def get_name_from_file(filename):
    # Dosya adından isim, soyisim ve ID'yi çıkarma
    base_name = os.path.basename(filename)
    name, surname, user_id, _ = base_name.split('_')  # Dosya adını bölüyoruz
    return name, surname, user_id  # İsim, soyad ve ID'yi döndürüyoruz

# Kamera ile yüz tanıma işlemini başlat
def start_face_recognition():
    recognizer = load_models()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kamera açılmadı.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Görüntü alınamadı.")
            break
        
        faces = detector.detect_faces(frame)

        for face in faces:
            x, y, w, h = face['box']
            face_img = frame[y:y+h, x:x+w]

            if face_img.size == 0:
                continue  

            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            resized_gray = cv2.resize(gray, (100, 100))

            try:
                label, confidence = recognizer.predict(resized_gray)

                # ID'ye göre kullanıcı bilgisi bul
                found = False
                for file in os.listdir("face_data"):
                    parts = file.split('_')
                    if len(parts) >= 3 and parts[2] == str(label):
                        name, surname = parts[0], parts[1]
                        found = True
                        break
                
                if found:
                    cv2.putText(frame, f"{name} {surname}",
                                (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Bilinmeyen", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            except cv2.error as e:
                print(f"Hata: {e}")
                continue

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()