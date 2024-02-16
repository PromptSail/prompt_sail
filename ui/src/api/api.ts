import { AxiosResponse } from 'axios';
import client from './client';
import {
    addProjectRequest,
    getAllProjects,
    getAllTransactionResponse,
    getProjectResponse,
    getProviders,
    getTransactionResponse,
    updateProjectRequest
} from './interfaces';

const api = {
    getProjects: (): Promise<AxiosResponse<getAllProjects[]>> => {
        return client.get('/api/projects');
    },
    getProject: (id: string): Promise<AxiosResponse<getProjectResponse>> => {
        return client.get(`/api/projects/${id}`);
    },
    getTransaction: (id: string): Promise<AxiosResponse<getTransactionResponse>> => {
        return client.get(`/api/transactions/${id}`);
    },
    getTransactions: (filters: string): Promise<AxiosResponse<getAllTransactionResponse>> => {
        return client.get(`/api/transactions${filters}`);
    },
    addProject: (data: addProjectRequest): Promise<AxiosResponse<any>> => {
        return client.post('/api/projects', data);
    },
    deleteProject: (id: string): Promise<AxiosResponse<any>> => {
        return client.delete(`/api/projects/${id}`);
    },
    updateProject: (id: string, data: updateProjectRequest): Promise<AxiosResponse<any>> => {
        return client.put(`/api/projects/${id}`, data);
    },
    getProviders: (): Promise<AxiosResponse<getProviders[]>> => {
        return client.get('/api/providers');
    }
};

export default api;
