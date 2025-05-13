import { Controller, Post, Body, UseInterceptors, UploadedFile, Get, Param } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { AppService } from './app.service';

@Controller('face')
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post('register')
  @UseInterceptors(FileInterceptor('image'))
  async registerFace(
    @UploadedFile() file: Express.Multer.File,
    @Body() body: { userId: string, angle: string }
  ) {
    return this.appService.registerFace(file, body.userId, body.angle);
  }

  @Get('verify/:userId')
  async verifyFace(@Param('userId') userId: string) {
    return this.appService.verifyFace(userId);
  }

  @Get('all-faces')
  async getAllFaces() {
    return this.appService.getAllFaces();
  }
}
