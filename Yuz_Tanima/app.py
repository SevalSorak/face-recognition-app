from collect_faces import collect_face_data, create_output_dir
from collect_user_data import collect_user_data
from recognize_faces import start_face_recognition
from train_model import train_face_model

def main():
    # Kullanıcı verilerini al ve isim, soyisim bilgilerini kaydet
    name, surname, user_id = collect_user_data()  

    # Çıktı dizinini oluştur
    create_output_dir("face_data")
    
    # Yüz verilerini topla
    collect_face_data(name=name, surname=surname, user_id=user_id,
                  output_dir="face_data",
                  directions=["Önden", "Sağ", "Sol"])

    # Yüz verilerini topla ve modeli eğit
    train_face_model(output_dir="face_data")

    # Yüz tanımayı başlat
    start_face_recognition()  # Yüz tanıma işlemi başlatılıyor

if __name__ == "__main__":
    main()
