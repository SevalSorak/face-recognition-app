import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { FaceModule } from 'src/face/face.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    FaceModule,
  ],
})
export class AppModule {}
