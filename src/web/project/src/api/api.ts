import axios, { AxiosResponse } from 'axios';
import client from './client';

const api = {
    getProjects: (): Promise<AxiosResponse<any>> => {
        return client.get('/api/projects');
    }
};

export default api;
