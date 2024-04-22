import { Flex, Typography, Layout, Button } from 'antd';
import { useState } from 'react';
import { getAllProjects } from '../../api/interfaces';
import { useGetAllProjects } from '../../api/queries';
import { PlusSquareOutlined } from '@ant-design/icons';
import outline from './../../assets/logo/symbol-teal-outline.svg';
import FilterDashboard from './FilterDashboard';

const { Title } = Typography;
const { Header } = Layout;

const Dashboard = () => {
    const projects = useGetAllProjects();
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [filter, _setFilter] = useState('');
    const filterProjects = (data: getAllProjects) => {
        return (
            data.name.includes(filter) ||
            data.slug.includes(filter) ||
            data.description.includes(filter) ||
            data.tags.join(', ').includes(filter)
        );
    };
    if (projects.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (projects.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(projects.error)}
            </>
        );
    if (projects.isSuccess) {
        const filteredProjects = projects.data.filter((el) => filterProjects(el));
        return (
            <Flex gap={24} vertical>
                <Header className="w-full min-h-[80px] border-0 border-b border-solid border-[#F0F0F0] relative overflow-hidden">
                    <Flex className="h-full" justify="space-between">
                        <div className="my-auto z-10">
                            <Title level={1} className="h4 m-auto">
                                Projects ({filteredProjects.length})
                            </Title>
                        </div>
                        <Button
                            className="my-auto z-10"
                            type="primary"
                            size="large"
                            icon={<PlusSquareOutlined />}
                        >
                            New project
                        </Button>
                    </Flex>
                    <img
                        src={outline}
                        className="absolute w-[390px] -bottom-[60px] right-14 opacity-60"
                    />
                </Header>
                <div className="px-[24px] max-w-[1600px] w-full mx-auto">
                    <FilterDashboard />
                </div>
                {/* <Flex vertical gap={30}>
                    <div
                        style={{
                            display: 'grid',
                            justifyContent: 'center',
                            gridTemplateColumns: 'repeat(auto-fill, 260px)',
                            padding: '.5rem 0',
                            gap: '20px'
                        }}
                    >
                        <Flex justify="space-between" style={{ gridColumn: '1 / -1' }}>
                            <Space align="end" size={15}>
                                <Title level={1} style={titleStyles}>
                                    Projects
                                </Title>
                                <Text style={textStyles}>1 members</Text>
                                <Text style={textStyles}>{projects.data.length} projects</Text>
                            </Space>
                            <Segmented
                                style={{ marginTop: 'auto' }}
                                defaultValue={dashView}
                                onChange={setDashView}
                                options={[
                                    {
                                        label: 'Kanban',
                                        value: 'kanban',
                                        icon: <AppstoreOutlined />
                                    },
                                    { label: 'List', value: 'list', icon: <BarsOutlined /> },
                                    { label: 'Table', value: 'table', icon: <TableOutlined /> }
                                ]}
                                disabled
                            />
                            <Input
                                type="text"
                                name="search"
                                placeholder="Search project (by name, tags, etc)"
                                onChange={(e) => {
                                    const val = e.currentTarget.value;
                                    if (val.length > 2) setFilter(val);
                                    else if (filter != '') setFilter('');
                                }}
                                style={{ marginTop: 'auto', maxWidth: '300px' }}
                            />
                        </Flex>
                        {dashView != 'table' && (
                            <>
                                <Link
                                    to="/projects/add"
                                    style={{
                                        gridColumn: `${dashView == 'list' ? '1 / -1' : 'auto'}`
                                    }}
                                >
                                    <Card
                                        hoverable
                                        className="h-full w-full"
                                        styles={{ body: { height: '100%' } }}
                                    >
                                        <Space className="h-full w-full justify-center">
                                            <Title
                                                level={2}
                                                className="!m-0 text-center opacity-50"
                                            >
                                                Add new project +
                                            </Title>
                                        </Space>
                                    </Card>
                                </Link>
                                {filteredProjects.map((e) => (
                                    <ProjectTile
                                        data={e}
                                        key={e.id}
                                        isListStyled={dashView == 'list'}
                                    />
                                ))}
                                {filteredProjects.length == 0 && (
                                    <h2 className="no-projects-found">No projects found</h2>
                                )}
                            </>
                        )}
                        {dashView == 'table' && <TableDashboard data={projects.data} />}
                    </div>
                </Flex> */}
            </Flex>
        );
    }
};

export default Dashboard;
