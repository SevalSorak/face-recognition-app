import { Injectable } from '@nestjs/common';
import { promises as fs } from 'fs';
import * as path from 'path';

@Injectable()
export class AppService {
  private readonly uploadDir = 'uploads';
  private readonly facesDir = 'faces';

  constructor() {
    this.ensureDirectories();
  }

  private async ensureDirectories() {
    await fs.mkdir(this.uploadDir, { recursive: true });
    await fs.mkdir(this.facesDir, { recursive: true });
  }

  async registerFace(
    file: Express.Multer.File,
    userId: string,
    angle: string
  ) {
    try {
      // Kullanıcı için klasör oluştur
      const userDir = path.join(this.facesDir, userId);
      await fs.mkdir(userDir, { recursive: true });

      // Dosyayı kaydet
      const fileName = `${angle}.jpg`;
      const filePath = path.join(userDir, fileName);
      await fs.writeFile(filePath, file.buffer);

      return {
        success: true,
        message: 'Yüz kaydı başarılı',
        data: {
          userId,
          angle,
          filePath
        }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Yüz kaydı başarısız',
        error: error?.message || 'Bilinmeyen hata'
      };
    }
  }

  async verifyFace(userId: string) {
    try {
      const userDir = path.join(this.facesDir, userId);
      const files = await fs.readdir(userDir);
      
      return {
        success: true,
        data: {
          userId,
          registeredAngles: files.map(f => f.replace('.jpg', ''))
        }
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Yüz doğrulama başarısız',
        error: error?.message || 'Bilinmeyen hata'
      };
    }
  }

  async getAllFaces() {
    try {
      const users = await fs.readdir(this.facesDir);
      const faces = [];

      for (const user of users) {
        const userDir = path.join(this.facesDir, user);
        const files = await fs.readdir(userDir);
        
        faces.push({
          userId: user,
          angles: files.map(f => f.replace('.jpg', ''))
        });
      }

      return {
        success: true,
        data: faces
      };
    } catch (error: any) {
      return {
        success: false,
        message: 'Yüz listesi alınamadı',
        error: error?.message || 'Bilinmeyen hata'
      };
    }
  }
}
