import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { FaceModule } from './face/face.module';

@Module({
  imports: [
    ConfigModule.forRoot(),
    FaceModule
  ],
})
export class AppModule {}
