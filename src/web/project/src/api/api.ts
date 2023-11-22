import axios, { AxiosResponse } from 'axios';
import client from './client';
import { addProjectRequest, updateProjectRequest } from './interfaces';

const api = {
    getProjects: (): Promise<AxiosResponse<any>> => {
        return client.get('/api/projects');
    },
    getProject: (id: string): Promise<AxiosResponse<any>> => {
        return client.get(`/api/project/${id}`);
    },
    addProject: (data: addProjectRequest): Promise<AxiosResponse<any>> => {
        return client.post('/api/project', data);
    },
    deleteProject: (id: string): Promise<AxiosResponse<any>> => {
        return client.delete(`/api/project/${id}`);
    },
    updateProject: (id: string, data: updateProjectRequest): Promise<AxiosResponse<any>> => {
        return client.post(`/api/project${id}/update`, data);
    }
};

export default api;
