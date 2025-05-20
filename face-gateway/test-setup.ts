import 'reflect-metadata';

// Jest için gerekli yapılandırmalar
jest.useFakeTimers();

// Test timeout süresini 30 saniye olarak ayarla
jest.setTimeout(30000);

// Test başlangıcında çalışacak hazırlık
beforeAll(() => {
  console.log('Test ortamı başlatılıyor...');
});

// Test sonunda çalışacak temizlik
afterAll(() => {
  console.log('Test ortamı kapatılıyor...');
}); 