from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
import os
import pickle
from PIL import Image
import io
import glob

app = Flask(__name__)
CORS(app)

FACE_DATA_DIR = "face_data"
MODEL_PATH = "trained_face_model.yml"
LABEL_MAP_PATH = "label_mappings.pkl"

def ensure_directories():
    os.makedirs(FACE_DATA_DIR, exist_ok=True)

def crop_square_face(img, x, y, w, h):
    size = max(w, h)
    center_x = x + w // 2
    center_y = y + h // 2
    half_size = size // 2

    left = max(0, center_x - half_size)
    top = max(0, center_y - half_size)
    right = min(img.shape[1], center_x + half_size)
    bottom = min(img.shape[0], center_y + half_size)

    if right - left != size:
        left = max(0, right - size)
    if bottom - top != size:
        top = max(0, bottom - size)

    return img[top:bottom, left:right]

def train_model():
    try:
        # LBPH modelini eğit
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
                    face_img = crop_square_face(img, x, y, w, h)

                    if face_img.shape[0] < 50 or face_img.shape[1] < 50:
                        continue

                    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    resized = cv2.resize(gray, (100, 100))
                    faces.append(resized)
                    labels.append(label_id)

            label_id += 1

        if faces:
            recognizer.train(faces, np.array(labels))
            recognizer.save(MODEL_PATH)
            with open(LABEL_MAP_PATH, "wb") as f:
                pickle.dump(label_to_user, f)
            print("✅ Model güncellendi")
            return True
        else:
            print("❌ Eğitim için yeterli veri yok")
            return False

    except Exception as e:
        print(f"❌ Model eğitimi hatası: {str(e)}")
        return False

@app.route('/register-face', methods=['POST'])
def register_face():
    try:
        print('form:', request.form)
        print('files:', request.files)
        files = request.files.getlist('image')
        user_id = request.form.get('userId')
        angle = request.form.get('angle')
        name = request.form.get('name')
        surname = request.form.get('surname')

        if not all([user_id, angle, name, surname]):
            return jsonify({"status": "error", "message": "Eksik bilgi"}), 400

        if not files or len(files) == 0:
            return jsonify({"status": "error", "message": "Görüntü bulunamadı"}), 400

        user_folder = f"{user_id}_{name}_{surname}"
        user_dir = os.path.join(FACE_DATA_DIR, user_folder)
        os.makedirs(user_dir, exist_ok=True)

        face_saved = False
        for idx, image_file in enumerate(files):
            image_bytes = image_file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            detector = MTCNN()
            results = detector.detect_faces(img)
            print('Algılanan yüz sayısı:', len(results))

            for result in results:
                x, y, w, h = result['box']
                x, y = max(0, x), max(0, y)
                face_img = crop_square_face(img, x, y, w, h)
                if face_img.shape[0] < 50 or face_img.shape[1] < 50:
                    continue

                # Her fotoğrafı sıralı kaydet
                face_path = os.path.join(user_dir, f"{angle}_{idx+1}.jpg")
                cv2.imwrite(face_path, face_img)
                face_saved = True

        if not face_saved:
            return jsonify({"status": "error", "message": "Yüz kaydedilemedi"}), 400

        # Tüm fotoğraflar yüklendikten sonra modeli eğit
        model_updated = train_model()

        return jsonify({
            "status": "success",
            "message": "Yüz(ler) başarıyla kaydedildi",
            "data": {
                "userId": user_id,
                "angle": angle,
                "name": name,
                "surname": surname,
                "modelUpdated": model_updated
            }
        }), 201

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "Görüntü bulunamadı"}), 400

        image_file = request.files['image']
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # DeepFace ile yüz tanıma
        results = DeepFace.find(
            img_path=img,
            db_path=FACE_DATA_DIR,
            model_name="Facenet",
            detector_backend="mtcnn",
            enforce_detection=False,
            distance_metric="euclidean_l2"
        )

        recognized_faces = []
        for result in results:
            if result.empty:
                continue

            identity = result["identity"].iloc[0]
            confidence = float(result["distance"].iloc[0])

            # Kullanıcı bilgilerini çıkar
            folder_name = os.path.basename(os.path.dirname(identity))
            try:
                user_id, name, surname = folder_name.split("_", 2)
            except:
                continue

            if confidence < 1.0:  # Güven eşiği
                recognized_faces.append({
                    "userId": user_id,
                    "name": name,
                    "surname": surname,
                    "confidence": confidence
                })

        if not recognized_faces:
            return jsonify({"status": "error", "message": "Yüz eşleşmesi bulunamadı"}), 404

        return jsonify({
            "status": "success",
            "faces": recognized_faces
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    ensure_directories()
    app.run(port=5001, debug=True)
