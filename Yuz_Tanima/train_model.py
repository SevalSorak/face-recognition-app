import cv2
import os
import numpy as np
import pickle
from mtcnn import MTCNN

def train_face_model(output_dir="face_data"):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = MTCNN()  

    faces = []
    labels = []
    label_to_user = {}
    label_id = 0

    for folder_name in sorted(os.listdir(output_dir)):
        folder_path = os.path.join(output_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Klasör adı: 123_Seval_Sorak
        try:
            user_id, name, surname = folder_name.split("_", 2)
        except:
            print(f"❌ Geçersiz klasör adı: {folder_name}")
            continue

        label_to_user[label_id] = {
            "user_id": user_id,
            "name": name,
            "surname": surname
        }

        for img_file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_file)
            img = cv2.imread(img_path)
            if img is None:
                continue

            # MTCNN ile yüz algılama
            results = detector.detect_faces(img)
            for result in results:
                x, y, w, h = result['box']
                x, y = max(0, x), max(0, y)
                face_img = img[y:y+h, x:x+w]
                if face_img.size == 0 or face_img.shape[0] < 50 or face_img.shape[1] < 50:
                    continue

                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                face_resized = cv2.resize(gray, (100, 100))
                faces.append(face_resized)
                labels.append(label_id)

        label_id += 1

    if faces:
        recognizer.train(faces, np.array(labels))
        recognizer.save("trained_face_model.yml")
        with open("label_mappings.pkl", "wb") as f:
            pickle.dump(label_to_user, f)
        print("✅ Model ve label eşlemeleri başarıyla kaydedildi.")

        # 💬 Label eşleşmelerini göster
        for label, user in label_to_user.items():
            print(f"🔢 Label {label} → {user['name']} {user['surname']}")
    else:
        print("❌ Eğitim için yeterli yüz verisi yok.")