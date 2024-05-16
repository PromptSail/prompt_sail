import { useNavigate, useParams } from 'react-router-dom';
import { useGetProject } from '../../api/queries';
import { getProjectResponse } from '../../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from './Update/UpdateProject';
import AddProject from './Add/AddProject';
import { Button, Flex, Typography } from 'antd';
import Container from '../../components/Container/Container';
import { TagsContainer } from '../../helpers/dataContainer';
import AiProvidersTable from './AiProvidersTable';
import LatestTransactions from './LatestTransactions';
import DeleteProject from '../../components/ProjectForms/DeleteProject';
import Statistics from './Statistics/Statistics';
import { NotificationInstance } from 'antd/es/notification/interface';
const { Title, Paragraph } = Typography;

interface AddProps {
    notification: NotificationInstance;
}

const Project: React.FC & { Add: React.FC<AddProps>; Update: React.FC } = () => {
    const navigate = useNavigate();
    const params = useParams();
    const project: UseQueryResult<AxiosResponse<getProjectResponse>> = useGetProject(
        params.projectId || ''
    );
    if (project.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (project.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(project.error)}
                {navigate('/')}
            </>
        );
    if (project.isSuccess) {
        const data = project.data.data;
        return (
            <>
                <Flex align="center" justify="space-between">
                    <Title style={{ margin: 5 }}>{data.name}</Title>
                    <Flex gap={10}>
                        <Button
                            type="primary"
                            onClick={() =>
                                window.open(
                                    'https://promptsail.github.io/prompt_sail/docs/project-dashboard/',
                                    '_blank'
                                )
                            }
                            ghost
                            style={{ background: '#FFF' }}
                        >
                            Help
                        </Button>
                        <Button
                            type="primary"
                            onClick={() => navigate(`/projects/${data.id}/update`)}
                        >
                            Edit
                        </Button>
                        <DeleteProject name={data.name} projectId={data.id} />
                    </Flex>
                </Flex>
                <Paragraph>{data.description}</Paragraph>
                <Flex gap={10}>
                    <Container
                        header="Basic info"
                        classname={{ parent: 'grow-0 shrink-0', box: 'w-[300px] gap-2.5' }}
                    >
                        <Flex justify="space-between">
                            <span>Members:</span>
                            <span>1</span>
                        </Flex>
                        <Flex justify="space-between">
                            <span>Total transactions:</span>
                            <span>{data.total_transactions}</span>
                        </Flex>
                        <Flex justify="space-between">
                            <span>Total cost:</span>
                            <span>{`$ ${data.total_cost.toFixed(4)}`}</span>
                        </Flex>
                        <Flex justify="space-between">
                            <span>Tags:</span>
                            <TagsContainer tags={data.tags} classname="justify-end" />
                        </Flex>
                    </Container>
                    <Container header="AI Providers" classname={{ parent: 'w-full' }}>
                        <AiProvidersTable providers={data.ai_providers} slug={data.slug} />
                    </Container>
                </Flex>

                <Statistics projectId={data.id} />
                <Container
                    header={
                        <Flex justify="space-between">
                            <Title level={2} style={{ margin: '0 10px' }}>
                                Latest transactions
                            </Title>
                            <Button
                                type="primary"
                                className="!bg-white my-auto"
                                onClick={() => navigate(`/transactions?project_id=${data.id}`)}
                                ghost
                            >
                                View all transactions
                            </Button>
                        </Flex>
                    }
                    classname={{ parent: 'my-5' }}
                >
                    <LatestTransactions projectId={data.id} />
                </Container>
            </>
        );
    }
};
Project.Add = AddProject;
Project.Update = UpdateProject;

export default Project;
