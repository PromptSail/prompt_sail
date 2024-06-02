import { useAddProject } from '../../../api/queries';
import ProjectForm from '../../../components/ProjectForms/ProjectForm';
import { FormikValuesTemplate } from '../../../components/ProjectForms/types';
import { Link, useNavigate } from 'react-router-dom';
import { Breadcrumb, Flex, Typography } from 'antd';
import HeaderContainer from '../../../components/HeaderContainer/HeaderContainer';
import { NotificationInstance } from 'antd/es/notification/interface';

const { Title } = Typography;

interface Props {
    notification: NotificationInstance;
}

const AddProject: React.FC<Props> = ({ notification }) => {
    const addProject = useAddProject();
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValuesTemplate) => {
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
                notification.success({
                    message: 'Success',
                    description: 'Project successfully added',
                    placement: 'bottomRight',
                    duration: 5
                });
            });
    };
    return (
        <Flex gap={24} vertical>
            <HeaderContainer height={100}>
                <Flex vertical justify="space-between">
                    <Breadcrumb
                        className="ms-1"
                        items={[
                            {
                                title: <Link to={'/projects'}>Projects</Link>
                            },
                            {
                                title: 'Create Project'
                            }
                        ]}
                    />
                    <Title level={1} className="h4 m-0">
                        Create Project
                    </Title>
                </Flex>
            </HeaderContainer>
            <ProjectForm formId="ProjectAdd" submitFunc={submit} />
        </Flex>
    );
};
export default AddProject;
