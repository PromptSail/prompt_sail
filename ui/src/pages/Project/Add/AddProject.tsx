import { useAddProject } from '../../../api/queries';
import ProjectForm from '../../../components/ProjectForms/ProjectForm';
import { FormikValues } from '../../../components/ProjectForms/types';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Typography } from 'antd';

const { Title } = Typography;

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
        <div className="w-full max-w-[800px] mx-auto flex flex-col gap-3">
            <div>
                <Title level={1} className="!m-0">
                    Create project
                </Title>
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
