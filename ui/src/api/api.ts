import { AxiosResponse } from 'axios';
import client from './client';
import {
    addProjectRequest,
    addUserRequest,
    getAllProjects,
    getAllTransactionResponse,
    getModels,
    getOrganizationsResponse,
    getProjectResponse,
    getProviders,
    getStatisticsTransactionsCost,
    getStatisticsTransactionsCount,
    getStatisticsTransactionsSpeed,
    getTransactionResponse,
    getUsers,
    loginUserRequest,
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
    },
    getPortfolio: (): Promise<AxiosResponse<any>> => {
        return client.get('/api/portfolio/details');
    },
    getPortfolio_projectsUsage: (params: string): Promise<AxiosResponse<any>> => {
        return client.get(`/api/portfolio/usage_in_time${params}`);
    },
    getPortfolio_tagsUsage: (params: string): Promise<AxiosResponse<any>> => {
        return client.get(`/api/portfolio/costs_by_tag${params}`);
    },
    addUser: (
        data: addUserRequest
    ): Promise<AxiosResponse<{ details: string } | (addUserRequest & { is_active: boolean })>> => {
        return client.post('/api/auth/register', data);
    },
    loginUser: (data: loginUserRequest): Promise<AxiosResponse<{ details: string } | string>> => {
        return client.post('/api/auth/login', data);
    },
    getOrganizations: (id: string): Promise<AxiosResponse<getOrganizationsResponse>> => {
        return client.get(`/api/organizations/user/${id}`);
    }
};

export default api;
