import { Link, useParams } from 'react-router-dom';
import { useGetProject, useUpdateProject } from '../../api/queries';
import { getProjectResponse } from '../../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from './Update/UpdateProject';
import AddProject from './Add/AddProject';
import { Breadcrumb, Flex, Spin, Tabs, Typography } from 'antd';
import Statistics from './Statistics/Statistics';
import { NotificationInstance } from 'antd/es/notification/interface';
import HeaderContainer from '../../components/HeaderContainer/HeaderContainer';
import { useEffect, useState } from 'react';
import ProjectDetails from './ProjectDetails';
import AiProvidersList from './AiProvidersList';
import ProjectTransactions from './ProjectTransactions';
import DeleteProject from '../../components/ProjectForms/DeleteProject';
import { Context } from '../../context/Context';
import { useContext } from 'react';
import Page404 from '../../components/errorPages/page404';
const { Title } = Typography;

interface AddProps {
    notification: NotificationInstance;
}

const Project: React.FC & { Add: React.FC<AddProps>; Update: React.FC } = () => {
    const { notification } = useContext(Context);
    const [currentTab, setCurrentTab] = useState('1');
    const params = useParams();
    const project: UseQueryResult<AxiosResponse<getProjectResponse>> = useGetProject(
        params.projectId || ''
    );
    const updateProject = useUpdateProject();
    useEffect(() => {
        project.refetch();
    }, [currentTab]);
    if (project.isLoading)
        return (
            <div className="w-full h-full relative">
                <Spin
                    size="large"
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                />
            </div>
        );
    if (project.isError) return <Page404 />;
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
                            className="header-tab min-w-[273px]"
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
                    <DeleteProject projectId={data.id} name={data.name} />
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
                            <AiProvidersList
                                list={data.ai_providers}
                                slug={data.slug}
                                onUpdateProviders={(newProviders) => {
                                    const updateData: Omit<
                                        typeof data,
                                        'id' | 'total_cost' | 'total_transactions'
                                    > = data;
                                    updateProject.mutate({
                                        id: data.id,
                                        data: {
                                            ...updateData,
                                            ai_providers: newProviders,
                                            org_id: data.org_id || ''
                                        }
                                    });
                                    notification?.success({
                                        message: 'Changes saved!',
                                        placement: 'topRight',
                                        duration: 5
                                    });
                                }}
                            />
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
