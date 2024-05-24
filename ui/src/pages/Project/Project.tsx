import { Link, useNavigate, useParams } from 'react-router-dom';
import { useGetProject } from '../../api/queries';
import { getProjectResponse } from '../../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from './Update/UpdateProject';
import AddProject from './Add/AddProject';
import { Breadcrumb, Button, Flex, Tabs, Typography } from 'antd';
import Statistics from './Statistics/Statistics';
import { NotificationInstance } from 'antd/es/notification/interface';
import HeaderContainer from '../../components/HeaderContainer/HeaderContainer';
import { useState } from 'react';
import { DeleteOutlined } from '@ant-design/icons';
import ProjectDetails from './ProjectDetails';
import AiProvidersList from './AiProvidersList';
import ProjectTransactions from './ProjectTransactions';
const { Title } = Typography;

interface AddProps {
    notification: NotificationInstance;
}

const Project: React.FC & { Add: React.FC<AddProps>; Update: React.FC } = () => {
    const navigate = useNavigate();
    const [currentTab, setCurrentTab] = useState('1');
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
            <Flex vertical>
                <HeaderContainer height={123.5}>
                    <Flex vertical>
                        <Flex vertical justify="space-between">
                            <Breadcrumb
                                className="ms-1"
                                items={[
                                    {
                                        title: <Link to={'/projects'}>Projects</Link>
                                    },
                                    {
                                        title: data.name
                                    }
                                ]}
                            />
                            <Title level={1} className="h4 m-0">
                                {data.name}
                            </Title>
                        </Flex>
                        <Tabs
                            defaultActiveKey={currentTab}
                            className="project-tab"
                            onChange={(activeKey) => setCurrentTab(activeKey)}
                            items={[
                                {
                                    key: '1',
                                    label: 'Overview'
                                },
                                {
                                    key: '2',
                                    label: 'AI Providers'
                                },
                                {
                                    key: '3',
                                    label: 'Transactions'
                                }
                            ]}
                        />
                    </Flex>
                    <Button className="my-auto z-10" icon={<DeleteOutlined />}>
                        Delete
                    </Button>
                </HeaderContainer>
                <div className="px-[24px] pt-[24px] max-w-[1600px] w-full mx-auto">
                    <Flex className="m-auto" vertical gap={12}>
                        {currentTab == '1' && (
                            <>
                                <ProjectDetails details={data} />
                                <Statistics projectId={data.id} />
                            </>
                        )}
                        {currentTab == '2' && (
                            <AiProvidersList list={data.ai_providers} slug={data.slug} />
                        )}
                        {currentTab == '3' && <ProjectTransactions projectId={data.id} />}
                    </Flex>
                </div>
            </Flex>
        );
    }
};
Project.Add = AddProject;
Project.Update = UpdateProject;

export default Project;
