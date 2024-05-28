import { useUpdateProject } from '../../../api/queries';
import ProjectForm from '../../../components/ProjectForms/ProjectForm';
import { useNavigate, useParams } from 'react-router-dom';
import { Button, Typography } from 'antd';
import { FormikValuesTemplate } from '../../../components/ProjectForms/types';

const { Title } = Typography;

const UpdateProject: React.FC = () => {
    const updateProject = useUpdateProject();
    const projectId = useParams().projectId || '';
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValuesTemplate) => {
        updateProject
            .mutateAsync(
                { id: projectId, data: values },
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
        <div className="w-full max-w-[800px] mx-auto flex flex-col gap-3">
            <Title level={1} className="!mt-0">
                Update project
            </Title>
            <ProjectForm formId="ProjectUpdate" submitFunc={submit} projectId={projectId} />
            <Button type="primary" htmlType="submit" form="ProjectUpdate" block>
                Update
            </Button>
        </div>
    );
};
export default UpdateProject;
