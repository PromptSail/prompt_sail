import { useUpdateProject } from '../../api/queries';
import { updateProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from 'react-bootstrap';

const UpdateProject: React.FC = () => {
    const updateProject = useUpdateProject();
    const projectId = useParams().projectId || '';
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValues) => {
        const reqValues: updateProjectRequest = {
            ...values,
            tags: values.tags.replace(/\s/g, '').split(',')
        };
        updateProject
            .mutateAsync(
                { id: projectId, data: reqValues },
                {
                    onError: (err) => {
                        alert(`${err.code} ${err.message}`);
                    }
                }
            )
            .then(() => {
                navigate(`/projects/${projectId}`);
            });
    };
    return (
        <div className="projectForm__update">
            <h1>Update project</h1>
            <ProjectForm formId="ProjectUpdate" submitFunc={submit} projectId={projectId} />
            <Button type="submit" variant="primary" size="lg" className="mt-2" form="ProjectUpdate">
                Update
            </Button>
        </div>
    );
};
export default UpdateProject;
