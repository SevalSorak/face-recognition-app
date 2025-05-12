from flask import Flask, request, jsonify
import os
from face_utils import add_face_api, recognize_face_api

app = Flask(__name__)

# Fotoğrafların kaydedileceği klasör
UPLOAD_FOLDER = r'flask_api\face_data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Flask sunucu aktif", "status": "OK"})

@app.route('/add-face', methods=['POST'])
def add_face():
    # 'image' dosyalarını alıyoruz
    files = request.files.getlist('image')  # Birden fazla fotoğraf alıyoruz
    name = request.form.get('name')
    surname = request.form.get('surname')
    user_id = request.form.get('user_id')

    # Gerekli verilerin eksik olup olmadığını kontrol ediyoruz
    if not files or not name or not surname or not user_id:
        return jsonify({'error': 'Eksik bilgi'}), 400

    # Her dosyayı tek tek kaydedip işleyelim
    results = []
    for file in files:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            results.append({"file": file.filename, "error": 'Geçersiz dosya formatı. Lütfen PNG veya JPG dosyası gönderin.'})
            continue

        # Yüz ekleme işlemi
        result = add_face_api(file, name, surname, user_id)
        results.append(result)

    # Eğer tüm işlemler başarılı olduysa
    if all(result.get("status") == "success" for result in results):
        return jsonify({"message": "Yüzler başarıyla eklendi", "data": results}), 200
    else:
        return jsonify({"error": "Yüz eklenirken hata oluştu", "data": results}), 500

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    # 'image' dosyalarını alıyoruz
    files = request.files.getlist('image')  # Birden fazla fotoğraf alıyoruz

    if not files:
        return jsonify({'error': 'Görsel gönderilmedi'}), 400

    # Fotoğraf işlemesi
    results = []
    for file in files:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            results.append({"file": file.filename, "error": 'Geçersiz dosya formatı. Lütfen PNG veya JPG dosyası gönderin.'})
            continue

        # Yüz tanıma işlemi
        result = recognize_face_api(file)
        results.append(result)

    # Eğer tüm tanıma işlemleri başarılı olduysa
    if all(result.get("status") == "success" for result in results):
        return jsonify({"message": "Yüzler başarıyla tanındı", "data": results}), 200
    else:
        return jsonify({"error": "Yüz tanıma sırasında hata oluştu", "data": results}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
