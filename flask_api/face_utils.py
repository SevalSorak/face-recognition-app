import os
import cv2
import time
import pickle
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
from PIL import Image
from io import BytesIO

# 📁 Kayıt dizini
FACE_DATA_DIR = "face_data"

# ✅ Gerekiyorsa klasör oluştur
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 🧠 Kullanıcıyı kaydetme fonksiyonu
def add_face_api(image_file, name, surname, user_id):
    ensure_dir(FACE_DATA_DIR)
    
    # Klasör adı: "123_Seval_Sorak"
    user_folder = f"{user_id}_{name}_{surname}".replace(" ", "_")
    user_path = os.path.join(FACE_DATA_DIR, user_folder)
    ensure_dir(user_path)

    # Görseli oku ve kaydet
    image = Image.open(image_file.stream).convert('RGB')
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    timestamp = int(time.time() * 1000)
    img_name = f"{name}_{surname}_{user_id}_{timestamp}.jpg"
    img_path = os.path.join(user_path, img_name)
    cv2.imwrite(img_path, img_cv)

    print(f"📸 Görsel kaydedildi: {img_path}")

    # Eğitimi tetikle
    train_model()

    return {"status": "success", "message": f"Görsel kaydedildi ve model güncellendi: {img_name}"}

# 🎯 Yüz tanıma fonksiyonu
def recognize_face_api(image_file):
    try:
        image = Image.open(image_file.stream).convert('RGB')
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        label_map = load_label_map()
        detector = "mtcnn"

        results = DeepFace.find(
            img_path=img_cv,
            db_path=FACE_DATA_DIR,
            model_name="Facenet",
            detector_backend=detector,
            enforce_detection=False,
            distance_metric="euclidean_l2"
        )

        recognized = []
        for result in results:
            if result.empty:
                continue

            identity = result["identity"].iloc[0]
            confidence = float(result["distance"].iloc[0])

            label = "Yok"
            name_text = "Bilinmeyen"

            for lbl, user in label_map.items():
                user_folder = f"{user['user_id']}_{user['name']}_{user['surname']}"
                if user_folder in identity:
                    label = lbl
                    name_text = f"{user['name']} {user['surname']}"
                    break

            if confidence < 1.0:
                recognized.append({
                    "label": label,
                    "name": name_text,
                    "confidence": confidence
                })

        if not recognized:
            return {"status": "error", "message": "Yüz eşleşmesi bulunamadı"}

        return {"status": "success", "results": recognized}

    except Exception as e:
        return {"status": "error", "message": f"Hata: {str(e)}"}

# 🏷 Label verilerini yükle
def load_label_map():
    with open("label_mappings.pkl", "rb") as f:
        return pickle.load(f)

# 🧠 LBPH eğitimi (mevcut kodun uyarlanmış hali)
def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = MTCNN()

    faces = []
    labels = []
    label_to_user = {}
    label_id = 0

    for folder_name in sorted(os.listdir(FACE_DATA_DIR)):
        folder_path = os.path.join(FACE_DATA_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        try:
            user_id, name, surname = folder_name.split("_", 2)
        except:
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

            results = detector.detect_faces(img)
            for result in results:
                x, y, w, h = result['box']
                x, y = max(0, x), max(0, y)
                face_img = img[y:y+h, x:x+w]

                if face_img.shape[0] < 50 or face_img.shape[1] < 50:
                    continue

                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (100, 100))
                faces.append(resized)
                labels.append(label_id)

        label_id += 1

    if faces:
        recognizer.train(faces, np.array(labels))
        recognizer.save("trained_face_model.yml")
        with open("label_mappings.pkl", "wb") as f:
            pickle.dump(label_to_user, f)
        print("✅ Model eğitildi.")
    else:
        print("❌ Yüz verisi bulunamadı. Eğitim başarısız.")
