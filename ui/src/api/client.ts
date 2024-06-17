import axios from 'axios';
import { ReactNode, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useError } from '../context/ErrorContext';

const client = axios.create({
    baseURL: `/api`,
    headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
    }
});

const AxiosInterceptor: React.FC<{ children: ReactNode }> = ({ children }) => {
    const navigate = useNavigate();
    const { hasServerError, setHasServerError } = useError();
    useEffect(() => {
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
                const status = error.response.status;
                if (status >= 400 && status < 500) {
                    localStorage.removeItem('PS_TOKEN');
                    navigate('/signin');
                }
                if (status >= 500) {
                    console.error(error);
                    setHasServerError(true);
                }
                return Promise.reject(error);
            }
        );
    }, [navigate]);
    return children;
};

export default client;
export { AxiosInterceptor };
