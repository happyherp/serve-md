import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 58649,
    cors: true,
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://localhost:50858',
        changeOrigin: true,
        secure: false,
      },
      '/health': {
        target: 'http://localhost:50858',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})