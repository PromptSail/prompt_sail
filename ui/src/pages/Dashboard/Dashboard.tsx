import { Flex, Typography, Layout, Button, Row, Col, Pagination } from 'antd';
import { useState } from 'react';
import { getAllProjects } from '../../api/interfaces';
import { useGetAllProjects } from '../../api/queries';
import { PlusSquareOutlined } from '@ant-design/icons';
import outline from './../../assets/logo/symbol-teal-outline.svg';
import FilterDashboard from './FilterDashboard';
import ProjectTile from '../../components/ProjectTile/ProjectTile';

const { Title } = Typography;
const { Header } = Layout;

const Dashboard = () => {
    const projects = useGetAllProjects();
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [filter, _setFilter] = useState('');
    const [pageData, setPageData] = useState({
        page: 1,
        size: 5
    });
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
                    <Row
                        justify="space-between"
                        className="flex-nowrap gap-[24px] mx-[24px] mt-[8px] mb-[4px]"
                    >
                        <Col className="max-w-[50%] min-w-[50%] w-full leading-5">Title:</Col>
                        <Col className="w-full leading-5">Owner:</Col>
                        <Col className="w-full text-end leading-5">Transactions:</Col>
                        <Col className="w-full text-end leading-5">Cost:</Col>
                    </Row>
                    <Flex vertical gap={8}>
                        {filteredProjects
                            .slice(
                                (pageData.page - 1) * pageData.size,
                                pageData.page * pageData.size
                            )
                            .map((e) => (
                                <ProjectTile data={e} key={e.id} />
                            ))}
                        {filteredProjects.length == 0 && (
                            <h2 className="no-projects-found">No projects found</h2>
                        )}
                    </Flex>
                    <Flex
                        justify="flex-end"
                        className="mt-[12px] px-[24px] py-[16px] min-w-[22px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px] text-end"
                    >
                        <Pagination
                            className="dashboard-pagination"
                            defaultPageSize={pageData.size}
                            pageSize={pageData.size}
                            onChange={(page, size) => setPageData({ page, size })}
                            pageSizeOptions={[5, 15, 30, 45, 60]}
                            showSizeChanger
                            total={filteredProjects.length}
                            hideOnSinglePage={filteredProjects.length < 11}
                        />
                    </Flex>
                </div>
            </Flex>
        );
    }
};

export default Dashboard;
