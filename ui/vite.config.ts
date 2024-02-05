import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dotenv from 'dotenv';

const createProxy = (url: string) => ({
    '/api': {
        target: url,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
    }
});

export default defineConfig(({ mode }) => {
    const env = { ...process.env, ...dotenv.config({ path: `.env.${mode}` }).parsed };
    return {
        plugins: [react()],
        server: {
            port: parseInt(env.PORT),
            proxy: createProxy(env.BACKEND_URL)
        },
        preview: {
            port: parseInt(env.PORT),
            proxy: createProxy(env.BACKEND_URL)
        }
    };
});
