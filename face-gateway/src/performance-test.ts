import { Test } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import supertest from 'supertest';
import { AppModule } from './app.module';
import * as fs from 'fs';
import * as path from 'path';

describe('Face Recognition Performance Test', () => {
  let app: INestApplication;
  const testImagePath = path.join(__dirname, 'test_face.jpg');

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();

    // Test görüntüsünün varlığını kontrol et
    if (!fs.existsSync(testImagePath)) {
      console.error(`Test görüntüsü bulunamadı: ${testImagePath}`);
      process.exit(1);
    }
  });

  afterAll(async () => {
    await app.close();
  });

  it('should measure face registration performance', async () => {
    console.log('\nYüz Kaydetme Performans Testi:');
    console.log('-'.repeat(50));

    const startTime = Date.now();

    const response = await supertest(app.getHttpServer())
      .post('/face/register')
      .attach('image', testImagePath)
      .field('userId', 'test_user')
      .field('name', 'Test')
      .field('surname', 'User')
      .field('angle', 'front');

    const endTime = Date.now();
    const duration = (endTime - startTime) / 1000; // saniye cinsinden

    console.log(`Kaydetme Süresi: ${duration.toFixed(2)} saniye`);
    console.log(`Durum Kodu: ${response.status}`);
    console.log('Yanıt:', response.body);
  });

  it('should measure face recognition performance', async () => {
    console.log('\nYüz Tanıma Performans Testi:');
    console.log('-'.repeat(50));

    const startTime = Date.now();

    const response = await supertest(app.getHttpServer())
      .post('/face/recognize')
      .attach('image', testImagePath);

    const endTime = Date.now();
    const duration = (endTime - startTime) / 1000; // saniye cinsinden

    console.log(`Tanıma Süresi: ${duration.toFixed(2)} saniye`);
    console.log(`Durum Kodu: ${response.status}`);
    console.log('Yanıt:', response.body);
  });
}); 