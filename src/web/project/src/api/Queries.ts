import { UseMutationResult, UseQueryResult, useMutation, useQuery } from 'react-query';
import api from './api';
import { AxiosError, AxiosResponse } from 'axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { getProjectResponse, updateProjectRequest } from './interfaces';

export const useGetAllProjects = (): UseQueryResult<getProjectResponse[], AxiosError> => {
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

export const useUpdateProject = (): UseMutationResult<
    AxiosResponse,
    AxiosError,
    updateProjectRequest
> => {
    return useMutation(
        async (obj) => {
            return await api.updateProject(obj);
        },
        {
            onSuccess: () => {
                toast.success('Project successfully edited', {
                    position: 'bottom-left',
                    theme: 'colored',
                    autoClose: 1000
                });
            }
        }
    );
};

export const useDeleteProject = (): UseMutationResult<AxiosResponse, AxiosError, string> => {
    const navigate = useNavigate();
    return useMutation(
        async (id) => {
            console.log(id);
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
