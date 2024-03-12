import { useAddProject } from '../../../api/queries';
import ProjectForm from '../../../components/ProjectForms/ProjectForm';
import { FormikValues } from '../../../components/ProjectForms/types';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from 'antd';

const AddProject: React.FC = () => {
    const addProject = useAddProject();
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValues) => {
        addProject
            .mutateAsync(
                { data: values },
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
        <div className="w-full max-w-[800px] m-auto flex flex-col gap-3">
            <div>
                <h1>Create project</h1>
                <Link to="https://promptsail.github.io/prompt_sail/docs/how-to-create-a-new-project">
                    How to create a new project
                </Link>
            </div>
            <ProjectForm formId="ProjectAdd" submitFunc={submit} />
            <Button type="primary" htmlType="submit" form="ProjectAdd" block>
                Create
            </Button>
        </div>
    );
};
export default AddProject;
