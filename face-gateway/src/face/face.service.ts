import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import axios from 'axios';
import FormData from 'form-data';
import * as fs from 'fs';

@Injectable()
export class FaceService {
  private readonly flaskServiceUrl: string;

  constructor(private configService: ConfigService) {
    const url = this.configService.get<string>('FLASK_SERVICE_URL');
    if (!url) {
      throw new Error('FLASK_SERVICE_URL environment variable is not set');
    }
    this.flaskServiceUrl = url;
  }

  async addFace(filePath: string, name: string, surname: string, userId: string): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('image', fs.createReadStream(filePath));
      formData.append('name', name);
      formData.append('surname', surname);
      formData.append('userId', userId);
      formData.append('angle', 'front');

      const response = await axios.post(`${this.flaskServiceUrl}/register-face`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Yüz kaydetme hatası: ${error?.message || 'Bilinmeyen hata'}`);
    }
  }

  async recognizeFace(filePath: string): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('image', fs.createReadStream(filePath));

      const response = await axios.post(`${this.flaskServiceUrl}/recognize-face`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Yüz tanıma hatası: ${error?.message || 'Bilinmeyen hata'}`);
    }
  }

  async addFaceBuffer(file: Express.Multer.File, name: string, surname: string, userId: string): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('image', file.buffer, {
        filename: file.originalname,
        contentType: file.mimetype,
      });
      formData.append('name', name);
      formData.append('surname', surname);
      formData.append('userId', userId);
      formData.append('angle', 'front');

      const response = await axios.post(`${this.flaskServiceUrl}/register-face`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Yüz kaydetme hatası: ${error?.message || 'Bilinmeyen hata'}`);
    }
  }

  async recognizeFaceBuffer(file: Express.Multer.File): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('image', file.buffer, {
        filename: file.originalname,
        contentType: file.mimetype,
      });

      const response = await axios.post(`${this.flaskServiceUrl}/recognize-face`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Yüz tanıma hatası: ${error?.message || 'Bilinmeyen hata'}`);
    }
  }

  async addMultipleFaces(files: Express.Multer.File[], name: string, surname: string, userId: string, angle: string): Promise<any> {
    try {
      const formData = new FormData();
      for (const file of files) {
        formData.append('image', file.buffer, {
          filename: file.originalname,
          contentType: file.mimetype,
        });
      }
      formData.append('name', name);
      formData.append('surname', surname);
      formData.append('userId', userId);
      formData.append('angle', angle);

      const response = await axios.post(`${this.flaskServiceUrl}/register-face`, formData, {
        headers: {
          ...formData.getHeaders(),
        },
      });

      return response.data;
    } catch (error: any) {
      throw new Error(`Yüz kaydetme hatası: ${error?.message || 'Bilinmeyen hata'}`);
    }
  }
}
