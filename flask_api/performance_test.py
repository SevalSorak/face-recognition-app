import time
import requests
import cv2
import numpy as np
from PIL import Image
import io
import os

def test_face_recognition(image_path):
    # Test görüntüsünü yükle
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Yüz tanıma süresini ölç
    start_time = time.time()
    
    # API'ye istek gönder
    response = requests.post(
        'http://localhost:5001/recognize-face',
        files={'image': ('test.jpg', image_data)}
    )
    
    end_time = time.time()
    recognition_time = end_time - start_time
    
    return {
        'status': response.status_code,
        'recognition_time': recognition_time,
        'response': response.json() if response.status_code == 200 else None
    }

def test_face_registration(image_path, user_id, name, surname, angle):
    # Test görüntüsünü yükle
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Yüz kaydetme süresini ölç
    start_time = time.time()
    
    # API'ye istek gönder
    response = requests.post(
        'http://localhost:5001/register-face',
        files={'image': ('test.jpg', image_data)},
        data={
            'userId': user_id,
            'name': name,
            'surname': surname,
            'angle': angle
        }
    )
    
    end_time = time.time()
    registration_time = end_time - start_time
    
    return {
        'status': response.status_code,
        'registration_time': registration_time,
        'response': response.json() if response.status_code == 200 else None
    }

def run_performance_test():
    print("Performans Testi Başlıyor...")
    print("-" * 50)
    
    # Test görüntüsü yolu
    test_image = "test_face.jpg"  # Test için bir yüz görüntüsü kullanın
    
    if not os.path.exists(test_image):
        print(f"Hata: {test_image} bulunamadı!")
        return
    
    # Yüz tanıma testi
    print("\nYüz Tanıma Testi:")
    recognition_result = test_face_recognition(test_image)
    print(f"Tanıma Süresi: {recognition_result['recognition_time']:.2f} saniye")
    print(f"Durum Kodu: {recognition_result['status']}")
    if recognition_result['response']:
        print(f"Yanıt: {recognition_result['response']}")
    
    # Yüz kaydetme testi
    print("\nYüz Kaydetme Testi:")
    registration_result = test_face_registration(
        test_image,
        "test_user",
        "Test",
        "User",
        "front"
    )
    print(f"Kaydetme Süresi: {registration_result['registration_time']:.2f} saniye")
    print(f"Durum Kodu: {registration_result['status']}")
    if registration_result['response']:
        print(f"Yanıt: {registration_result['response']}")

if __name__ == "__main__":
    run_performance_test() 