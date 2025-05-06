from collect_faces import collect_face_data, create_output_dir
from collect_user_data import collect_user_data
from recognize_faces import start_face_recognition
from train_model import train_face_model

def main():
    name, surname, user_id = collect_user_data()

    create_output_dir("face_data")

    collect_face_data(name=name, surname=surname, user_id=user_id,
                      output_dir="face_data",
                      directions=["Önden", "Sağ", "Sol"])

    train_face_model(output_dir="face_data")
    start_face_recognition()

if __name__ == "__main__":
    main()
