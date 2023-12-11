import { useFormik } from 'formik';
import { useState } from 'react';
import { Button } from 'react-bootstrap';
import { useAddProject } from '../../api/queries';
import { addProjectRequest } from '../../api/interfaces';
import { addProjectSchema } from '../../api/formSchemas';
import { UseQueryResult } from 'react-query';
import ProjectForm from './ProjectForm';

interface Props {
    queryToRefetch: UseQueryResult;
}

const AddProject: React.FC<Props> = ({ queryToRefetch }) => {
    const [showModal, setShowModal] = useState(false);
    const addProject = useAddProject();
    const formik = useFormik({
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
            const reqValues: addProjectRequest = {
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
            addProject.mutateAsync({ data: reqValues }).then(() => {
                queryToRefetch.refetch();
                setShowModal((e) => !e);
            });
        },
        validateOnChange: true,
        validationSchema: addProjectSchema
    });
    return (
        <>
            <Button
                variant="primary"
                className="m-auto whitespace-nowrap"
                onClick={() => setShowModal((e) => !e)}
            >
                New Project +
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
export default AddProject;
