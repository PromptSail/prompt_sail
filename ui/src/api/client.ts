import axios from 'axios';
import { ReactNode } from 'react';
import { useError } from '../context/ErrorContext';
import { useLogin } from '../context/LoginContext';

const client = axios.create({
    baseURL: `/api`,
    headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
    }
});

const AxiosInterceptor: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { setLoginState } = useLogin();
    const { hasServerError, setHasServerError } = useError();
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
            if (!hasServerError) setHasServerError(false);
            return response;
        },
        (error) => {
            console.error('inter response error');
            console.error(error);
            const status = error.response.status;
            if (status === 401) {
                localStorage.removeItem('PS_TOKEN');
                setLoginState(false);
            } else {
                setHasServerError(true);
            }
            return Promise.reject(error);
        }
    );
    return children;
};

export default client;
export { AxiosInterceptor };
