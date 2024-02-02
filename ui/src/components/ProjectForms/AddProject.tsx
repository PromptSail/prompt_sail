import { useAddProject } from '../../api/queries';
import { addProjectRequest } from '../../api/interfaces';
import ProjectForm from './ProjectForm';
import { FormikValues } from './types';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const AddProject: React.FC = () => {
    const addProject = useAddProject();
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValues) => {
        const reqValues: addProjectRequest = {
            ...values,
            tags: values.tags.replace(/\s/g, '').split(',')
        };
        addProject.mutateAsync({ data: reqValues }).then(() => {
            navigate('/');
        });
    };
    return (
        <div className="project__add">
            <h3>Create project</h3>
            <ProjectForm formId="ProjectAdd" submitFunc={submit} />
            <Button type="submit" className="mt-2" form="ProjectAdd">
                Create
            </Button>
        </div>
    );
};
export default AddProject;
