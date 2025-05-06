from flask import Flask, request, jsonify
from face_utils import add_face_api, recognize_face_api

app = Flask(__name__)

@app.route('/add-face', methods=['POST'])
def add_face():
    file = request.files.get('image')
    name = request.form.get('name')
    surname = request.form.get('surname')
    user_id = request.form.get('user_id')

    if not file or not name or not surname or not user_id:
        return jsonify({'error': 'Eksik bilgi'}), 400

    result = add_face_api(file, name, surname, user_id)
    return jsonify(result)

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    file = request.files.get('image')

    if not file:
        return jsonify({'error': 'Görsel gönderilmedi'}), 400

    result = recognize_face_api(file)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
