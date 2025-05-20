import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { FaceController } from './face.controller';
import { FaceService } from './face.service';

@Module({
  imports: [ConfigModule],
  controllers: [FaceController],
  providers: [FaceService],
  exports: [FaceService]
})
export class FaceModule {} 