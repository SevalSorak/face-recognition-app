import requests

url = "http://localhost:5000/recognize-face"

# Daha önce kayıt ettiğin bir yüz görseli kullan (örnek: face_data/1705_seval_sorak/...)
image_path = r"face_data/1705_seval_sorak/seval_sorak_1705_1746538503323.jpg"

files = {'image': open(image_path, 'rb')}

response = requests.post(url, files=files)

try:
    print(response.json())
except Exception as e:
    print("Yanıt çözümlenemedi:", e)
