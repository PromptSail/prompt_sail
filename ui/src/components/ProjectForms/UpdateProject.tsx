import { useUpdateProject } from '../../api/queries';
import { updateProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
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
            <h3>Update project</h3>
            <ProjectForm formId="ProjectUpdate" submitFunc={submit} projectId={projectId} />
            <button type="submit" className="mt-2" form="ProjectUpdate">
                Update
            </button>
        </div>
    );
};
export default UpdateProject;
