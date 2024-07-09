import { UseMutationResult, UseQueryResult, useMutation, useQuery } from 'react-query';
import api from './api';
import { AxiosError, AxiosResponse } from 'axios';
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
    getStatisticsTransactionsSpeed,
    getLoggedUser,
    getUsers,
    getConfig,
    getModels
} from './interfaces';
import { StatisticsParams, TransactionsFilters } from './types';

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
    return useMutation(
        async (id) => {
            return await api.deleteProject(id);
        },
        {
            onError: (err) => {
                console.error(`${err.code}: ${err.message}`);
            }
        }
    );
};
export const useGetProviders = (): UseQueryResult<getProviders[], AxiosError> => {
    return useQuery(
        'providers',
        async () => {
            return (await api.getProviders()).data;
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
export const useGetConfig = (): UseQueryResult<AxiosResponse<getConfig>, AxiosError> => {
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
export const useWhoami = (): UseQueryResult<AxiosResponse<getLoggedUser>, AxiosError> => {
    return useQuery('whoami', async () => await api.whoami(), {
        staleTime: Infinity,
        retry: false,
        cacheTime: 0,
        refetchOnWindowFocus: false
    });
};
export const useGetUsers = (): UseQueryResult<AxiosResponse<getUsers[]>, AxiosError> => {
    return useQuery('users', async () => await api.getUsers(), {
        staleTime: Infinity,
        retry: false,
        cacheTime: 0,
        refetchOnWindowFocus: false
    });
};
export const useGetModels = (): UseQueryResult<getModels[], AxiosError> => {
    return useQuery('models', async () => (await api.getModels()).data, {
        staleTime: Infinity,
        retry: false,
        cacheTime: 0,
        refetchOnWindowFocus: false
    });
};
export const useGetPortfolio = (): UseQueryResult<any, AxiosError> => {
    return useQuery('portfolio', async () => (await api.getPortfolio()).data, {
        staleTime: Infinity,
        retry: false,
        cacheTime: 0,
        refetchOnWindowFocus: false
    });
};
export const useGetProjectsUsage = (
    params: Omit<StatisticsParams, 'project_id'>
): UseQueryResult<any[], AxiosError> => {
    return useQuery(
        ['portfolio_projectUsage', params],
        async () => (await api.getPortfolio_projectsUsage(linkParamsParser(params))).data,
        {
            enabled: !!params,
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};
export const useGetTagsUsage = (
    params: Omit<StatisticsParams, 'project_id'>
): UseQueryResult<any[], AxiosError> => {
    return useQuery(
        ['portfolio_tagsUsage', params],
        async () => (await api.getPortfolio_tagsUsage(linkParamsParser(params))).data,
        {
            enabled: !!params,
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};
