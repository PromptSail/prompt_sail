import { useNavigate, useParams } from 'react-router-dom';
import { useGetProject } from '../../api/queries';
import { getProjectResponse } from '../../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from './Update/UpdateProject';
import AddProject from './Add/AddProject';
import { Button, Flex, Typography } from 'antd';
import Container from './Container';
import { TagsContainer } from '../../helpers/dataContainer';
import AiProvidersTable from './AiProvidersTable';
import LatestTransactions from './LatestTransactions';
import DeleteProject from '../../components/ProjectForms/DeleteProject';
const { Title, Paragraph } = Typography;

const Project: React.FC & { Add: React.FC; Update: React.FC } = () => {
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
                        <Button type="primary" onClick={() => navigate('/projects/add')}>
                            Edit
                        </Button>
                        <DeleteProject name={data.name} projectId={data.id} />
                    </Flex>
                </Flex>
                <Paragraph>{data.description}</Paragraph>
                <Flex gap={10}>
                    <Container header="Basic info" classname="grow-0 shrink-0 w-[300px]">
                        <Flex justify="space-between">
                            <span>Members:</span>
                            <span>1</span>
                        </Flex>
                        <Flex justify="space-between">
                            <span>Total tranasction:</span>
                            <span>{data.total_transactions}</span>
                        </Flex>
                        <Flex justify="space-between">
                            <span>Total const:</span>
                            <span>$ 1.00</span>
                        </Flex>
                        <Flex justify="space-between">
                            <span>Tags:</span>
                            <TagsContainer tags={data.tags} classname="justify-end" />
                        </Flex>
                    </Container>
                    <Container header="Ai Providers" classname="w-full">
                        <AiProvidersTable providers={data.ai_providers} slug={data.slug} />
                    </Container>
                </Flex>
                <Container header="Last transactions">
                    <LatestTransactions projectId={data.id} />
                </Container>
            </>
        );
    }
};
Project.Add = AddProject;
Project.Update = UpdateProject;

export default Project;
