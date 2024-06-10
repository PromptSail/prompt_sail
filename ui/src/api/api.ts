import { AxiosResponse } from 'axios';
import client from './client';
import {
    addProjectRequest,
    getAllProjects,
    getAllTransactionResponse,
    getModels,
    getProjectResponse,
    getProviders,
    getStatisticsTransactionsCost,
    getStatisticsTransactionsCount,
    getStatisticsTransactionsSpeed,
    getTransactionResponse,
    getUsers,
    updateProjectRequest
} from './interfaces';

const api = {
    whoami: (): Promise<AxiosResponse> => {
        return client.get('/api/auth/whoami');
    },
    config: (): Promise<AxiosResponse> => {
        return client.get('/api/config');
    },
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
    },
    getStatistics_TransactionsCount: (
        params: string
    ): Promise<AxiosResponse<getStatisticsTransactionsCount[]>> => {
        return client.get(`/api/statistics/transactions_count${params}`);
    },
    getStatistics_TransactionsCost: (
        params: string
    ): Promise<AxiosResponse<getStatisticsTransactionsCost[]>> => {
        return client.get(`/api/statistics/transactions_cost${params}`);
    },
    getStatistics_TransactionsSpeed: (
        params: string
    ): Promise<AxiosResponse<getStatisticsTransactionsSpeed[]>> => {
        return client.get(`/api/statistics/transactions_speed${params}`);
    },
    getUsers: (): Promise<AxiosResponse<getUsers[]>> => {
        return client.get('/api/users');
    },
    getModels: (): Promise<AxiosResponse<getModels>> => {
        return client.get('/api/statistics/pricelist');
    }
};

export default api;
