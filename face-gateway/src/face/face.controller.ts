import { Controller, Post, UploadedFile, UseInterceptors, Body, UploadedFiles } from '@nestjs/common';
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';
import { FaceService } from './face.service';
import { memoryStorage } from 'multer';

@Controller('face')
export class FaceController {
  constructor(private readonly faceService: FaceService) {}

  @Post('register-face')
  @UseInterceptors(FilesInterceptor('image', 50, { storage: memoryStorage() }))
  async registerFace(
    @UploadedFiles() files: Express.Multer.File[],
    @Body('name') name: string,
    @Body('surname') surname: string,
    @Body('userId') userId: string,
    @Body('angle') angle: string,  // Swift’ten array olarak gelirse
  ) {
    // Açıklama: angle, birden fazla görsel için farklı açılar göndermek istersen array olur
    return this.faceService.addMultipleFaces(files, name, surname, userId, angle);
  }

  @Post('recognize-face')
  @UseInterceptors(FileInterceptor('image', { storage: memoryStorage() }))
  async recognizeFace(@UploadedFile() file: Express.Multer.File) {  
    return this.faceService.recognizeFaceBuffer(file);
  }
}
