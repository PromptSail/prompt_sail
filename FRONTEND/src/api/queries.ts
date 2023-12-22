import { UseMutationResult, UseQueryResult, useMutation, useQuery } from 'react-query';
import api from './api';
import { AxiosError, AxiosResponse } from 'axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import {
    TransactionResponse,
    addProjectRequest,
    getAllProjects,
    getProjectResponse,
    updateProjectRequest
} from './interfaces';

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
): UseQueryResult<AxiosResponse<TransactionResponse>, AxiosError> => {
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

export const useGetAllTransactions = (): UseQueryResult<
    AxiosResponse<TransactionResponse[]>,
    AxiosError
> => {
    return useQuery(
        'transactions',
        async () => {
            return await api.getTransactions();
        },
        {
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
                toast.success('Project successfully added', {
                    position: 'bottom-left',
                    autoClose: 1000,
                    theme: 'colored'
                });
            },
            onError: (err) => {
                console.error(err);
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
                toast.success('Project successfully edited', {
                    position: 'bottom-left',
                    theme: 'colored',
                    autoClose: 1000
                });
            },
            onError: (err) => {
                console.error(err);
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
                toast.info('Project successfully deleted', {
                    position: 'bottom-left',
                    theme: 'colored',
                    autoClose: 1000
                });
                navigate('/');
            }
        }
    );
};
