import { useFormik } from 'formik';
import { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import { UseQueryResult } from 'react-query';
import { updateProjectRequest } from '../../api/interfaces';
import { useUpdateProject } from '../../api/queries';
import { AxiosResponse } from 'axios';
import ProjectForm from './ProjectForm';

interface Props {
    projectId: string;
    queryToRefetch: UseQueryResult<AxiosResponse>;
}

const UpdateProject: React.FC<Props> = ({ projectId, queryToRefetch }) => {
    const [showModal, setShowModal] = useState(false);
    const updateProject = useUpdateProject();
    const formik = useFormik({
        enableReinitialize: true,
        initialValues: {
            name: '',
            slug: '',
            description: '',
            api_base: '',
            provider_name: '',
            ai_model_name: '',
            tags: '',
            org_id: ''
        },
        onSubmit: async ({
            name,
            slug,
            description,
            api_base,
            provider_name,
            ai_model_name,
            tags,
            org_id
        }) => {
            const reqValues: updateProjectRequest = {
                id: projectId,
                name,
                slug,
                description,
                ai_providers: [
                    {
                        api_base,
                        provider_name,
                        ai_model_name
                    }
                ],
                tags: tags.replace(/\s/g, '').split(','),
                org_id
            };
            updateProject.mutateAsync({ id: projectId, data: reqValues }).then(() => {
                queryToRefetch.refetch();
                setShowModal((e) => !e);
            });
        }
    });
    useEffect(() => {
        if (queryToRefetch.isSuccess) {
            const data = queryToRefetch.data.data;
            formik.setValues({
                name: data.name,
                slug: data.slug,
                description: data.description,
                api_base: data.ai_providers[0].api_base,
                provider_name: data.ai_providers[0].provider_name,
                ai_model_name: data.ai_providers[0].ai_model_name,
                tags: data.tags.join(', '),
                org_id: data.org_id || ''
            });
        }
    }, [queryToRefetch.isSuccess]);
    return (
        <>
            <Button variant="primary" onClick={() => setShowModal((e) => !e)}>
                Edit
            </Button>
            <ProjectForm
                handleChange={formik.handleChange}
                handleSubmit={formik.handleSubmit}
                values={formik.values}
                showHandler={{
                    isShow: showModal,
                    setShow: setShowModal
                }}
            />
        </>
    );
};
export default UpdateProject;
