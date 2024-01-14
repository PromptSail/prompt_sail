import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
    process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
    return {
        plugins: [react()],
        server: {
            port: parseInt(process.env.PORT),
            proxy: {
                '/api': {
                    target: process.env.BACKEND_URL || 'http://promptsail.local:8000',
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, '')
                }
            }
        },
        preview: {
            port: parseInt(process.env.PORT),
            proxy: {
                '/api': {
                    target: process.env.BACKEND_URL || 'http://promptsail-backend:8000',
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, '')
                }
            }
        }
    };
});
