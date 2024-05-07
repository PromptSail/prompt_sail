import axios from 'axios';

const client = axios.create({
    baseURL: `/api`,
    headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
    }
});

client.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('PS_TOKEN');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        console.error('inter request error');
        return Promise.reject(error);
    }
);

client.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        console.error('inter response error');
        const status = error.response.status;
        if (status >= 400 && status < 500) {
            localStorage.removeItem('PS_TOKEN');
            window.location.replace('/signin');
        }
        return Promise.reject(error);
    }
);

export default client;
