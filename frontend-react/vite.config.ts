import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendTarget = env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

  const proxyConfig = {
    '/api': { target: backendTarget, changeOrigin: true },
    '/login': { target: backendTarget, changeOrigin: true },
    '/logout': { target: backendTarget, changeOrigin: true },
    '/dashboard': { target: backendTarget, changeOrigin: true },
    '/students': { target: backendTarget, changeOrigin: true },
    '/daily-reports': { target: backendTarget, changeOrigin: true },
    '/assessments': { target: backendTarget, changeOrigin: true },
    '/gallery': { target: backendTarget, changeOrigin: true },
    '/evaluations': { target: backendTarget, changeOrigin: true },
    '/reports': { target: backendTarget, changeOrigin: true },
    '/users': { target: backendTarget, changeOrigin: true },
    '/static': { target: backendTarget, changeOrigin: true },
  }

  return {
    plugins: [react()],
    server: {
      host: true, // Izinkan akses dari perangkat lain dalam jaringan lokal
      port: 5173,
      proxy: proxyConfig,
    },
    preview: {
      host: true,
      port: 4173,
      proxy: proxyConfig,
    },
  }
})
