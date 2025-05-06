import cv2
import os
import pickle
from deepface import DeepFace
import numpy as np
import json

def load_models():
    # label_mappings.pkl dosyasını yükle
    with open("label_mappings.pkl", "rb") as f:
        label_map = pickle.load(f)
    # DeepFace için veri tabanı yolunu hazırla
    face_data_dir = "face_data"
    return face_data_dir, label_map

def start_face_recognition():
    face_data_dir, label_map = load_models()
    # DeepFace dedektörü (MTCNN kullanıyoruz, alternatif: opencv, dlib)
    detector = "mtcnn"
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            # DeepFace ile yüz tanıma
            results = DeepFace.find(
                img_path=frame,
                db_path=face_data_dir,
                model_name="Facenet",
                detector_backend=detector,
                enforce_detection=False,
                distance_metric="euclidean_l2"
            )
            
            # Her algılanan yüz için işlem yap
            for result in results:
                if result.empty:
                    continue
                    
                # Yüz koordinatlarını al
                x = int(result["source_x"].iloc[0])
                y = int(result["source_y"].iloc[0])
                w = int(result["source_w"].iloc[0])
                h = int(result["source_h"].iloc[0])
                
                # Küçük yüzleri filtrele
                if w < 50 or h < 50:
                    continue

                # Kimlik dosya yolunu al
                identity = result["identity"].iloc[0]
                # Güven skoru (mesafe, düşük değer daha iyi)
                confidence = result["distance"].iloc[0]
                
                # label_map ile eşleştir
                label = None
                for lbl, user_info in label_map.items():
                    user_folder = f"{user_info['user_id']}_{user_info['name']}_{user_info['surname']}"
                    if user_folder in identity:
                        label = lbl
                        break
                
                if label is not None and confidence < 1.0:  # DeepFace için güven eşiği (1.0 uygun bir başlangıç)
                    user_info = label_map.get(label, {"name": "Bilinmeyen", "surname": ""})
                    name_text = f"{user_info['name']} {user_info['surname']}"
                else:
                    name_text = "Bilinmeyen"
                
                # Çıktıyı önceki formatta yazdır
                print(f"Yüz koordinatları: ({x}, {y}, {w}, {h}) | Tahmin: {label if label is not None else 'Yok'} | Güven: {confidence:.2f}")
                print(f"[CONF] Tahmin: {label if label is not None else 'Yok'} - Güven: {confidence:.2f}")

                # Dikdörtgen ve isim çiz
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        except Exception as e:
            print(f"Hata: {e}")
            name_text = "Tanımlanamadı"
            # Hata durumunda devam et
            continue

        cv2.imshow("Yüz Tanıma", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_face(image_path):
    face_data_dir, label_map = load_models()
    detector = "mtcnn"  # Alternatif: "opencv" veya "dlib"

    try:
        frame = cv2.imread(image_path)
        if frame is None:
            return {"status": "error", "message": "Görüntü okunamadı"}

        results = DeepFace.find(
            img_path=frame,
            db_path=face_data_dir,
            model_name="Facenet",
            detector_backend=detector,
            enforce_detection=False,
            distance_metric="euclidean_l2"
        )

        recognized_faces = []
        for result in results:
            if result.empty:
                continue

            x = int(result["source_x"].iloc[0])
            y = int(result["source_y"].iloc[0])
            w = int(result["source_w"].iloc[0])
            h = int(result["source_h"].iloc[0])
            if w < 50 or h < 50:
                continue

            identity = result["identity"].iloc[0]
            confidence = result["distance"].iloc[0]

            label = None
            for lbl, user_info in label_map.items():
                user_folder = f"{user_info['user_id']}_{user_info['name']}_{user_info['surname']}"
                if user_folder in identity:
                    label = lbl
                    break

            if label is not None and confidence < 1.0:
                user_info = label_map.get(label, {"name": "Bilinmeyen", "surname": ""})
                name_text = f"{user_info['name']} {user_info['surname']}"
            else:
                name_text = "Bilinmeyen"
                label = "Yok"

            recognized_faces.append({
                "coordinates": {"x": x, "y": y, "w": w, "h": h},
                "label": label,
                "confidence": float(confidence),
                "name": name_text
            })

        if not recognized_faces:
            return {"status": "error", "message": "Yüz algılanmadı veya eşleşme bulunamadı"}

        return {
            "status": "success",
            "faces": recognized_faces
        }

    except Exception as e:
        return {"status": "error", "message": f"Hata: {str(e)}"}