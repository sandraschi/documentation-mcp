import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
            allowedHosts: ['goliath'],
        port: 11032,
        strictPort: true,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:11033',
                changeOrigin: true,
            },
            '/docs': {
                target: 'http://127.0.0.1:11033',
                changeOrigin: true,
            },
            '/openapi.json': {
                target: 'http://127.0.0.1:11033',
                changeOrigin: true,
            },
            '/redoc': {
                target: 'http://127.0.0.1:11033',
                changeOrigin: true,
            },
        }
    }
})
