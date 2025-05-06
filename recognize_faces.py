import cv2
import os
import pickle
from mtcnn import MTCNN

def load_models():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trained_face_model.yml")
    with open("label_mappings.pkl", "rb") as f:
        label_map = pickle.load(f)
    return recognizer, label_map

def start_face_recognition():
    recognizer, label_map = load_models()
    detector = MTCNN()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kamera açılamadı.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detector.detect_faces(frame)
        for face in faces:
            x, y, w, h = face['box']
            x, y = max(0, x), max(0, y)
            face_img = frame[y:y+h, x:x+w]
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (100, 100))

            try:
                label, confidence = recognizer.predict(resized)
                print(f"Yüz koordinatları: ({x}, {y}, {w}, {h}) | Tahmin: {label} | Güven: {confidence:.2f}")
                if confidence < 80:  # Eşik değeri (80'i deneysel olarak ayarlayabilirsiniz)
                    user_info = label_map.get(label, {"name": "Bilinmeyen", "surname": ""})
                    name_text = f"{user_info['name']} {user_info['surname']}"
                else:
                    name_text = "Bilinmeyen"

                print(f"[CONF] Tahmin: {label} - Güven: {confidence:.2f}")
                user_info = label_map.get(label, {"name": "Bilinmeyen", "surname": ""})
                name_text = f"{user_info['name']} {user_info['surname']}"
            except:
                name_text = "Tanımlanamadı"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Yüz Tanıma", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()