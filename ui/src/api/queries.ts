import { UseMutationResult, UseQueryResult, useMutation, useQuery } from 'react-query';
import api from './api';
import { AxiosError, AxiosResponse } from 'axios';
import { useNavigate } from 'react-router-dom';
import {
    getAllTransactionResponse,
    addProjectRequest,
    getAllProjects,
    getProjectResponse,
    updateProjectRequest,
    getTransactionResponse,
    getProviders
} from './interfaces';
import { TransactionsFilters } from './types';
import { notification } from 'antd';

export const useGetAllProjects = (): UseQueryResult<getAllProjects[], AxiosError> => {
    return useQuery(
        'projects',
        async () => {
            return (await api.getProjects()).data;
        },
        {
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};
export const useGetProject = (
    id: string
): UseQueryResult<AxiosResponse<getProjectResponse>, AxiosError> => {
    return useQuery(
        'project',
        async () => {
            return await api.getProject(id);
        },
        {
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};

export const useGetTransaction = (
    id: string
): UseQueryResult<AxiosResponse<getTransactionResponse>, AxiosError> => {
    return useQuery(
        'transaction',
        async () => {
            return await api.getTransaction(id);
        },
        {
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};

export const useGetAllTransactions = (
    filters: TransactionsFilters
): UseQueryResult<AxiosResponse<getAllTransactionResponse>, AxiosError> => {
    let filters_str = '?';
    Object.keys(filters).forEach((key) => {
        const val = filters[key as keyof TransactionsFilters];
        if (`${val}`.length > 0) {
            if (filters_str.length > 1) filters_str += '&';
            filters_str += `${key}=${val}`;
        }
    });
    return useQuery(
        ['transactions', filters],
        async () => {
            return await api.getTransactions(filters_str);
        },
        {
            enabled: !!filters,
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};

export const useAddProject = (): UseMutationResult<
    AxiosResponse,
    AxiosError,
    { data: addProjectRequest }
> => {
    return useMutation(
        async ({ data }) => {
            return await api.addProject(data);
        },
        {
            onSuccess: () => {
                notification.success({
                    message: 'Success',
                    description: 'Project successfully added',
                    placement: 'bottomRight',
                    duration: 5
                });
            },
            onError: (err) => {
                console.error(`${err.code}: ${err.message}`);
            }
        }
    );
};

export const useUpdateProject = (): UseMutationResult<
    AxiosResponse,
    AxiosError,
    { id: string; data: updateProjectRequest }
> => {
    return useMutation(
        async ({ id, data }) => {
            return await api.updateProject(id, data);
        },
        {
            onSuccess: () => {
                notification.success({
                    message: 'Success',
                    description: 'Project successfully edited',
                    placement: 'bottomRight',
                    duration: 5
                });
            },
            onError: (err) => {
                console.error(`${err.code}: ${err.message}`);
            }
        }
    );
};

export const useDeleteProject = (): UseMutationResult<AxiosResponse, AxiosError, string> => {
    const navigate = useNavigate();
    return useMutation(
        async (id) => {
            return await api.deleteProject(id);
        },
        {
            onSuccess: () => {
                notification.warning({
                    message: 'Success',
                    description: 'Project successfully deleted',
                    placement: 'bottomRight',
                    duration: 5
                });
                navigate('/');
            },
            onError: (err) => {
                console.error(`${err.code}: ${err.message}`);
            }
        }
    );
};
export const useGetProviders = (): UseQueryResult<AxiosResponse<getProviders[]>, AxiosError> => {
    return useQuery(
        'providers',
        async () => {
            return await api.getProviders();
        },
        {
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: false
        }
    );
};
