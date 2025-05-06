import { Module } from '@nestjs/common';
import { FaceService } from './face/face.service';
import { FaceController } from './face/face.controller';

@Module({
  imports: [],
  controllers: [FaceController],
  providers: [FaceService],
})
export class AppModule {}
