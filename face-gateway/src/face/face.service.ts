import { Injectable } from '@nestjs/common';
import axios, { AxiosResponse } from 'axios';
import FormData from 'form-data';
import * as fs from 'fs';

interface RecognitionResult {
  confidence: number;
  label: number;
  name: string;
}

interface RecognitionResponse {
  results: RecognitionResult[];
  status: string;
}

interface AddFaceResponse {
  message: string;
  status: string;
}

@Injectable()
export class FaceService {
  async addFace(imagePath: string, name: string, surname: string, userId: string) {
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath));
    form.append('name', name);
    form.append('surname', surname);
    form.append('user_id', userId);

    const response: AxiosResponse<AddFaceResponse> = await axios.post('https://e0f6-159-146-84-133.ngrok-free.app/add-face', form, {
      headers: form.getHeaders(),
    });

    return response.data;
  }

  async recognizeFace(imagePath: string) {
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath));

    const response: AxiosResponse<RecognitionResponse> = await axios.post('hhttps://e0f6-159-146-84-133.ngrok-free.app/recognize-face', form, {
      headers: form.getHeaders(),
    });

    return response.data;
  }
}
