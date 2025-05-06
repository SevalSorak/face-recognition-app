import cv2
from datetime import datetime

# Fotoğrafı kaydetme
def save_face_image(face_image, name, surname, age, user_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"face_data/{name}_{surname}_{user_id}_{timestamp}.jpg"  # user_id'yi ekliyoruz
    cv2.imwrite(filename, face_image)
    return filename  # Fotoğraf yolunu döndürüyoruz

# Kullanıcıdan bilgi alma ve fotoğraf kaydetme
def collect_user_data():
    name = input("Adınızı girin: ")
    surname = input("Soyadınızı girin: ")
    age = input("Yaşınızı girin: ")

    # Kullanıcıya ID atama (bunu daha gelişmiş bir şekilde veritabanı ile yapabilirsiniz)
    user_id = hash(name + surname) % 10000  # Örnek: isim ve soyadına göre ID oluşturma

    # Kamera açma ve fotoğraf çekme işlemi
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        photo = save_face_image(frame, name, surname, age, user_id)  # Fotoğrafı kaydediyoruz
    else:
        print("Fotoğraf çekilemedi!")
    camera.release()

    return name, surname, user_id  # Artık ID de döndürüyoruz

