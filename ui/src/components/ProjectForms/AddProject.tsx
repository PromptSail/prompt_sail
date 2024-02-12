import { useAddProject } from '../../api/queries';
import { addProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
import { useNavigate } from 'react-router-dom';

const AddProject: React.FC = () => {
    const addProject = useAddProject();
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValues) => {
        const reqValues: addProjectRequest = {
            ...values,
            tags: values.tags.replace(/\s/g, '').split(',')
        };
        addProject
            .mutateAsync(
                { data: reqValues },
                {
                    onError: (err) => {
                        alert(`${err.code} ${err.message}`);
                    }
                }
            )
            .then(() => {
                navigate('/');
            });
    };
    return (
        <div className="projectForm__add">
            <h3>Create project</h3>
            <ProjectForm formId="ProjectAdd" submitFunc={submit} />
            <button type="submit" className="mt-2" form="ProjectAdd">
                Create
            </button>
        </div>
    );
};
export default AddProject;
