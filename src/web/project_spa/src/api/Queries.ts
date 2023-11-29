import { UseMutationResult, UseQueryResult, useMutation, useQuery } from 'react-query';
import api from './api';
import { AxiosResponse } from 'axios';
import { toast } from 'react-toastify';
import { Navigate, redirect, useNavigate, useRoutes } from 'react-router-dom';

export const useGetAllProjects = (): UseQueryResult<any> => {
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
export const useGetProject = (id: string | undefined): UseQueryResult<any> => {
    return useQuery(
        'project',
        async () => {
            return await api.getProject(id || '');
        },
        {
            staleTime: Infinity,
            retry: false,
            cacheTime: 0,
            refetchOnWindowFocus: 'always'
        }
    );
};

export const useUpdateProject = (): UseMutationResult<any> => {
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

export const useDeleteProject = (): UseMutationResult<any> => {
    const navigate = useNavigate();
    return useMutation(
        async (obj) => {
            return await api.deleteProject(obj.projectId);
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
