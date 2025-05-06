import { Controller, Post, UploadedFile, UseInterceptors, Body } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { FaceService } from './face.service';
import { diskStorage } from 'multer';
import { extname } from 'path';

@Controller('face')
export class FaceController {
  constructor(private readonly faceService: FaceService) {}

  @Post('add')
  @UseInterceptors(
    FileInterceptor('image', {
      storage: diskStorage({
        destination: './uploads',
        filename: (_, file, cb) => {
          const unique = Date.now() + extname(file.originalname);
          cb(null, file.fieldname + '-' + unique);
        },
      }),
    }),
  )
  async addFace(
    @UploadedFile() file: Express.Multer.File,
    @Body('name') name: string,
    @Body('surname') surname: string,
    @Body('user_id') userId: string,
  ) {
    return this.faceService.addFace(file.path, name, surname, userId);
  }

  @Post('recognize')
  @UseInterceptors(
    FileInterceptor('image', {
      storage: diskStorage({
        destination: './uploads',
        filename: (_, file, cb) => {
          const unique = Date.now() + extname(file.originalname);
          cb(null, file.fieldname + '-' + unique);
        },
      }),
    }),
  )
  async recognizeFace(@UploadedFile() file: Express.Multer.File) {
    return this.faceService.recognizeFace(file.path);
  }
}
