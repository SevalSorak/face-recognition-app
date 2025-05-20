# Yüz Tanıma Projesi

Bu proje, yüz tanıma teknolojisini kullanarak çoklu platform desteği sunan bir sistemdir. Proje, Python, Node.js ve iOS bileşenlerinden oluşmaktadır.

## Proje Yapısı

Proje dört ana bileşenden oluşmaktadır:

### 1. Face Recognition Python (`face_recognition_python/`)
Yüz tanıma sisteminin temel Python implementasyonu. Bu modül şunları içerir:
- Yüz verisi toplama (`collect_faces.py`)
- Model eğitimi (`train_model.py`)
- Yüz tanıma işlemleri (`recognize_faces.py`)
- Kullanıcı verisi toplama (`collect_user_data.py`)

### 2. Face Gateway (`face-gateway/`)
Node.js tabanlı API gateway servisi. NestJS framework'ü kullanılarak geliştirilmiştir.
- TypeScript ile geliştirilmiş
- REST API endpoints
- Dosya yükleme işlemleri
- Test altyapısı

### 3. Flask API (`flask_api/`)
Python Flask tabanlı API servisi. Yüz tanıma işlemlerini gerçekleştiren backend servisi.
- Yüz tanıma işlemleri
- Yüz işleme yardımcı fonksiyonları

### 4. iOS Uygulaması (`ios/`)
iOS platformu için mobil uygulama.

## Kurulum

### Face Recognition Python
```bash
cd face_recognition_python
pip install -r requirements.txt
```

### Face Gateway
```bash
cd face-gateway
npm install
```

### Flask API
```bash
cd flask_api
pip install -r requirements.txt
```

## Kullanım

1. Önce yüz verilerini toplayın:
```bash
python face_recognition_python/collect_faces.py
```

2. Modeli eğitin:
```bash
python face_recognition_python/train_model.py
```

3. Face Gateway'i başlatın:
```bash
cd face-gateway
npm run start
```

4. Flask API'yi başlatın:
```bash
cd flask_api
python app.py
```

## Geliştirme

- Face Gateway için test yazımı: `npm run test`

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 