import cv2
import os
import numpy as np
import unicodedata
from mtcnn import MTCNN

# Yüz verilerini kaydedeceğiniz dizin
def create_output_dir(output_dir="face_data"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# Yüz verilerini normalize et (Türkçe karakterlerden arındır)
def rename_files(directory):
    for filename in os.listdir(directory):
        normalized_name = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
        os.rename(os.path.join(directory, filename), os.path.join(directory, normalized_name))

# Yüz tanıma modeli eğitme
def train_face_model(output_dir="face_data"):
    # LBPH yüz tanıma modeli
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # MTCNN yüz tespit modeli
    detector = MTCNN()

    faces = []
    labels = []

    # Dosya adlarını normalize et
    rename_files(output_dir)

    # Görsel yollarını topla
    image_paths = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.lower().endswith(('.jpg', '.png'))]

    if not image_paths:
        print("❌ Klasörde yüz görseli bulunamadı.")
        return False

    for image_path in image_paths:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Hata: {image_path} okunamadı.")
            continue

        # MTCNN ile yüz algılama
        detected_faces = detector.detect_faces(img)
        if not detected_faces:
            print(f"⚠️ Yüz bulunamadı: {image_path}")
            continue

        for detected_face in detected_faces:
            try:
                x, y, w, h = detected_face['box']
                x, y = max(0, x), max(0, y)  # Negatif koordinatlara karşı koruma
                face = img[y:y+h, x:x+w]
                face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face_resized = cv2.resize(face_gray, (100, 100))  # Boyut sabitle
                faces.append(face_resized)

                # Etiketi dosya adından çek (örnek: isim_soyisim_1746467879_493.jpg → 1746467879)
                parts = os.path.basename(image_path).split('_')
                label = int(parts[2]) if len(parts) >= 3 else 0
                labels.append(label)

            except Exception as e:
                print(f"⚠️ Hata oluştu ({image_path}): {e}")
                continue

    if faces and labels and len(faces) == len(labels):
        recognizer.train(faces, np.array(labels))
        recognizer.save("trained_face_model.yml")
        print("✅ Model başarıyla eğitildi ve 'trained_face_model.yml' olarak kaydedildi.")
        return True
    else:
        print("❌ Eğitim için yeterli yüz verisi veya geçerli etiket bulunamadı.")
        print(f"Yüz sayısı: {len(faces)}, Etiket sayısı: {len(labels)}")
        return False

