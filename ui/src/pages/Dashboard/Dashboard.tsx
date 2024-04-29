import { Flex, Typography, Layout, Button, Row, Col, Pagination } from 'antd';
import { useEffect, useState } from 'react';
import { getAllProjects } from '../../api/interfaces';
import { useGetAllProjects } from '../../api/queries';
import { PlusSquareOutlined } from '@ant-design/icons';
import outline from './../../assets/logo/symbol-teal-outline.svg';
import FilterDashboard from './FilterDashboard';
import ProjectTile from '../../components/ProjectTile/ProjectTile';

const { Title, Text } = Typography;
const { Header } = Layout;

const Dashboard = () => {
    const projects = useGetAllProjects();
    const [filter, setFilter] = useState('');
    const [pageData, setPageData] = useState({
        page: 1,
        size: 5
    });
    const [paginationInfo, setPaginationInfo] = useState('');
    const [filteredProjects, setFilteredProjects] = useState<getAllProjects[]>([]);
    type range = {
        start: number | null;
        end: number | null;
    };
    const [isAsc, setAsc] = useState(false);
    const [sortby, setSortby] = useState<string>('title');
    const [costRange, setCostRange] = useState<range>({ start: null, end: null });
    const [transactionsRange, setTransactionsRange] = useState<range>({ start: null, end: null });
    const inSearch = (data: getAllProjects) => {
        return data.name.includes(filter) || data.tags.join(', ').includes(filter);
    };
    const inCostRange = (data: getAllProjects) => {
        const { start, end } = costRange;
        if (start == null || end == null) return true;
        return data.total_cost >= start && data.total_cost <= end;
    };
    const inTransactionsRange = (data: getAllProjects) => {
        const { start, end } = transactionsRange;
        if (start == null || end == null) return true;
        return data.total_transactions >= start && data.total_transactions <= end;
    };
    const sortInterpreter = (arg: string, a: getAllProjects, b: getAllProjects) => {
        switch (arg) {
            case 'title':
                return a.name > b.name ? 1 : -1;
            case 'transactions':
                return a.total_transactions - b.total_transactions;
            case 'cost':
                return a.total_cost - b.total_cost;
            default:
                return 0;
        }
    };
    useEffect(() => {
        if (projects.isSuccess) {
            const filteredData = projects.data
                .filter((el) => inSearch(el) && inCostRange(el) && inTransactionsRange(el))
                .sort((a, b) => {
                    const asc = isAsc ? 1 : -1;
                    return sortInterpreter(sortby, a, b) * asc;
                })
                .slice((pageData.page - 1) * pageData.size, pageData.page * pageData.size);
            setFilteredProjects(filteredData);
            setPaginationInfo(
                `Showing ${(pageData.page - 1) * pageData.size}-${
                    pageData.page * pageData.size
                } of ${filteredData.length}`
            );
        }
    }, [projects.status, pageData, costRange, transactionsRange, isAsc, sortby, filter]);
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
        const maxCost = projects.data.reduce(
            (max, current) => (current.total_cost > max ? current.total_cost : max),
            0
        );
        const maxTransactionsCount = projects.data.reduce(
            (max, current) => (current.total_transactions > max ? current.total_transactions : max),
            0
        );
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
                    <FilterDashboard
                        costRange={{ ...costRange, max: maxCost }}
                        transactionsRange={{
                            ...transactionsRange,
                            max: maxTransactionsCount
                        }}
                        onSearch={setFilter}
                        onSortAsc={setAsc}
                        onSortByChange={setSortby}
                        onChangeCost={setCostRange}
                        onChangeTransactions={setTransactionsRange}
                        onSetOwner={function (): void {
                            throw new Error('Function not implemented.');
                        }}
                    />
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
                        {filteredProjects.map((e) => (
                            <ProjectTile data={e} key={e.id} />
                        ))}
                        {filteredProjects.length == 0 && (
                            <h2 className="no-projects-found">No projects found</h2>
                        )}
                    </Flex>
                    <Flex
                        justify="flex-end"
                        gap={10}
                        className="mt-[12px] px-[24px] py-[16px] min-w-[22px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px] text-end"
                    >
                        <Text className="my-auto">{paginationInfo}</Text>
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
