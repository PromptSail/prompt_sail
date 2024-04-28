import { Flex, Input, Space, Typography, Card, Segmented } from 'antd';
import { CSSProperties, useState } from 'react';
import ProjectTile from '../../components/ProjectTile/ProjectTile';
import { getAllProjects } from '../../api/interfaces';
import { useGetAllProjects } from '../../api/queries';
import { AppstoreOutlined, BarsOutlined, TableOutlined } from '@ant-design/icons';
import TableDashboard from './TableDashboard';
import { Link } from 'react-router-dom';

const { Title, Text } = Typography;

const Dashboard = () => {
    const textStyles: CSSProperties = { lineHeight: '2em' };
    const titleStyles: CSSProperties = { margin: '0' };
    const [dashView, setDashView] = useState('list');
    const projects = useGetAllProjects();
    const [filter, setFilter] = useState('');
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
            <>
                <Flex vertical gap={30}>
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
                </Flex>
            </>
        );
    }
};

export default Dashboard;
