import { Injectable } from '@nestjs/common';
import axios from 'axios';
import * as FormData from 'form-data';
import * as fs from 'fs';

@Injectable()
export class FaceService {
  async addFace(imagePath: string, name: string, surname: string, userId: string) {
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath));
    form.append('name', name);
    form.append('surname', surname);
    form.append('user_id', userId);

    const response = await axios.post('http://localhost:5000/add-face', form, {
      headers: form.getHeaders(),
    });

    return response.data;
  }

  async recognizeFace(imagePath: string) {
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath));

    const response = await axios.post('http://localhost:5000/recognize-face', form, {
      headers: form.getHeaders(),
    });

    return response.data;
  }
}
