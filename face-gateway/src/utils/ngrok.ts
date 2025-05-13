import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';

export async function updateNgrokUrl() {
  try {
    // Ngrok'un web arayüzünden URL'yi al
    const response = await fetch('http://localhost:4040/api/tunnels');
    const data = await response.json();
    
    if (data.tunnels && data.tunnels.length > 0) {
      const ngrokUrl = data.tunnels[0].public_url;
      
      // .env dosyasını oku
      const envPath = path.resolve(process.cwd(), '.env');
      let envContent = fs.readFileSync(envPath, 'utf8');
      
      // NGROK_URL değerini güncelle
      if (envContent.includes('NGROK_URL=')) {
        envContent = envContent.replace(/NGROK_URL=.*/g, `NGROK_URL=${ngrokUrl}`);
      } else {
        envContent += `\nNGROK_URL=${ngrokUrl}`;
      }
      
      // .env dosyasını güncelle
      fs.writeFileSync(envPath, envContent);
      
      console.log(`✅ Ngrok URL güncellendi: ${ngrokUrl}`);
      return ngrokUrl;
    }
  } catch (error) {
    console.error('❌ Ngrok URL alınamadı:', error);
  }
  return null;
} 