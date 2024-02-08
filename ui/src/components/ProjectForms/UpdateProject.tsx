import { useUpdateProject } from '../../api/queries';
import { updateProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
import { Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';

const UpdateProject: React.FC = () => {
    const updateProject = useUpdateProject();
    const projectId = useParams().projectId || '';
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValues) => {
        const reqValues: updateProjectRequest = {
            ...values,
            tags: values.tags.replace(/\s/g, '').split(',')
        };
        updateProject.mutateAsync({ id: projectId, data: reqValues }).then(() => {
            navigate(`/projects/${projectId}`);
        });
    };
    return (
        <div className="projectForm__update">
            <h3>Update project</h3>
            <ProjectForm formId="ProjectUpdate" submitFunc={submit} projectId={projectId} />
            <Button type="submit" className="mt-2" form="ProjectUpdate">
                Update
            </Button>
        </div>
    );
};
export default UpdateProject;
