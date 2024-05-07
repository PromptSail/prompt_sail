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
    const env = {
        ...dotenv.config({ path: `.env.${mode}` }).parsed,
        ...process.env
    };
    console.log('using env', env);
    return {
        plugins: [react()],
        server: {
            port: parseInt(env.PORT),
            proxy: createProxy(env.BACKEND_URL)
        },
        preview: {
            port: parseInt(env.PORT),
            proxy: createProxy(env.BACKEND_URL)
        },
        define: {
            'import.meta.env.PROXY_URL_HOST': new String(env.PROXY_URL_HOST),
            SSO_GOOGLE_ID: new String(env.SSO_GOOGLE_CLIENT_ID),
            SSO_AZURE: {
                CLIENT_ID: new String(env.SSO_AZURE_CLIENT_ID),
                TENANT: new String(env.SSO_AZURE_TENANT),
                SCOPES: new String(env.SSO_AZURE_SCOPES).split(','),
                AUTHORITY: new String(env.SSO_AZURE_AUTHORITY)
            }
        }
    };
});
