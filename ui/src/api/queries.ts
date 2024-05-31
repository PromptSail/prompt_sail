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
    getProviders,
    getStatisticsTransactionsCount,
    getStatisticsTransactionsCost,
    getStatisticsTransactionsSpeed
} from './interfaces';
import { StatisticsParams, TransactionsFilters } from './types';
import { notification } from 'antd';

const linkParamsParser = <T extends { [key: string]: string }>(params: T): string => {
    let paramsStr = '?';
    Object.keys(params).forEach((key) => {
        const val = params[key as keyof T];
        if (`${val}`.length > 0) {
            if (paramsStr.length > 1) paramsStr += '&';
            paramsStr += `${key}=${val}`;
        }
    });
    return paramsStr;
};

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
    return useQuery(
        ['transactions', filters],
        async () => {
            return await api.getTransactions(linkParamsParser(filters));
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
export const useGetStatistics_TransactionsCount = (
    params: StatisticsParams
): UseQueryResult<AxiosResponse<getStatisticsTransactionsCount[]>, AxiosError> => {
    return useQuery(
        ['statistics_transactionsCount', params],
        async () => {
            return await api.getStatistics_TransactionsCount(linkParamsParser(params));
        },
        {
            enabled: !!params,
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};
export const useGetStatistics_TransactionsCost = (
    params: StatisticsParams
): UseQueryResult<AxiosResponse<getStatisticsTransactionsCost[]>, AxiosError> => {
    return useQuery(
        ['statistics_transactionsCost', params],
        async () => {
            return await api.getStatistics_TransactionsCost(linkParamsParser(params));
        },
        {
            enabled: !!params,
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};
export const useGetStatistics_TransactionsSpeed = (
    params: StatisticsParams
): UseQueryResult<AxiosResponse<getStatisticsTransactionsSpeed[]>, AxiosError> => {
    return useQuery(
        ['statistics_transactionsSpeed', params],
        async () => {
            return await api.getStatistics_TransactionsSpeed(linkParamsParser(params));
        },
        {
            enabled: !!params,
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};
export const useGetConfig = (): UseQueryResult<
    AxiosResponse<{
        organization: string;
        authorization: boolean;
        azure_auth: boolean;
        google_auth: boolean;
    }>,
    AxiosError
> => {
    return useQuery(
        'config',
        async () => {
            return await api.config();
        },
        {
            staleTime: 10000,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: false
        }
    );
};
