import { useAddProject } from '../../api/queries';
import { addProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';

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
            <h1>Create project</h1>
            <ProjectForm formId="ProjectAdd" submitFunc={submit} />
            <Button type="submit" variant="primary" size="lg" form="ProjectAdd">
                Create
            </Button>
        </div>
    );
};
export default AddProject;
