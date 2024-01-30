import { useUpdateProject } from '../../api/queries';
import { updateProjectRequest } from '../../api/interfaces';
import { addProjectSchema } from '../../api/formSchemas';
import ProjectForm from '../../pages/ProjectForm';
import { FormikValues } from './types';
import { Button } from 'react-bootstrap';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useEffect } from 'react';

const UpdateProject: React.FC = () => {
    const updateProject = useUpdateProject();
    const projectId = useParams().projectId || '';
    const navigate = useNavigate();
    const { state } = useLocation();
    const submit = async (values: typeof FormikValues) => {
        const reqValues: updateProjectRequest = {
            ...values,
            tags: values.tags.replace(/\s/g, '').split(',')
        };
        updateProject.mutateAsync({ id: projectId, data: reqValues }).then(() => {
            navigate(`/projects/${projectId}`);
        });
    };
    useEffect(() => {
        if (state === null) navigate(`/projects/${projectId}`);
    });
    return (
        <div className="project__update">
            <ProjectForm
                formId="ProjectUpdate"
                submitFunc={submit}
                validationSchema={addProjectSchema}
                project={state.project}
            />
            <Button type="submit" className="mt-2" form="ProjectUpdate">
                Update
            </Button>
        </div>
    );
};
export default UpdateProject;
