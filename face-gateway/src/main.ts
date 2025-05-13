import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import 'reflect-metadata';
import * as dotenv from 'dotenv';
import { updateNgrokUrl } from './utils/ngrok';

// .env dosyasını yükle
dotenv.config();

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // CORS ayarları
  app.enableCors({
    origin: '*',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    allowedHeaders: 'Content-Type, Accept',
  });

  // Global prefix
  app.setGlobalPrefix('api');

  const port = process.env.PORT || 5000;
  await app.listen(port);
  
  // Ngrok URL'sini güncelle
  const ngrokUrl = await updateNgrokUrl() || process.env.NGROK_URL;
  
  console.log(`🚀 Uygulama ${port} portunda çalışıyor`);
  if (ngrokUrl) {
    console.log(`🌐 Ngrok URL: ${ngrokUrl}`);
  } else {
    console.log('⚠️ Ngrok URL bulunamadı. Lütfen ngrok\'u başlatın veya .env dosyasında NGROK_URL değişkenini ayarlayın.');
  }
}
bootstrap();
