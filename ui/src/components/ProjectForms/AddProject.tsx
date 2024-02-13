import { useAddProject } from '../../api/queries';
import { addProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
import { Link, useNavigate } from 'react-router-dom';
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
            <div>
                <h1>Create project</h1>
                <Link to="https://promptsail.github.io/prompt_sail/docs/how-to-create-a-new-project">
                    How to create a new project
                </Link>
            </div>
            <ProjectForm formId="ProjectAdd" submitFunc={submit} />
            <Button type="submit" variant="primary" size="lg" form="ProjectAdd">
                Create
            </Button>
        </div>
    );
};
export default AddProject;
