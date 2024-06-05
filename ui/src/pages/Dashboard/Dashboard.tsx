import { Flex, Typography, Button, Row, Col, Pagination } from 'antd';
import { useContext, useEffect, useState } from 'react';
import { getAllProjects } from '../../api/interfaces';
import { useGetAllProjects } from '../../api/queries';
import { PlusSquareOutlined } from '@ant-design/icons';
import FilterDashboard from './FilterDashboard';
import ProjectTile from '../../components/ProjectTile/ProjectTile';
import noFoundImg from '../../assets/paper_boat.svg';
import noResultsImg from '../../assets/loupe.svg';
import { useNavigate } from 'react-router-dom';
import HeaderContainer from '../../components/HeaderContainer/HeaderContainer';
import { Context } from '../../context/Context';

const { Title, Text } = Typography;

const Dashboard = () => {
    const projects = useGetAllProjects();
    const auth = useContext(Context).config?.authorization;
    const [filter, setFilter] = useState('');
    const [filterOwner, setFilterOwner] = useState<string | null>(null);
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
    const inOwner = (data: getAllProjects) => {
        return filterOwner ? data.owner === filterOwner : true;
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
    const navigate = useNavigate();
    useEffect(() => {
        if (projects.isSuccess) {
            const filteredData = projects.data
                .filter(
                    (el) =>
                        inSearch(el) && inCostRange(el) && inTransactionsRange(el) && inOwner(el)
                )
                .sort((a, b) => {
                    const asc = isAsc ? 1 : -1;
                    return sortInterpreter(sortby, a, b) * asc;
                });
            setFilteredProjects(filteredData);
            setPaginationInfo(
                `Showing ${(pageData.page - 1) * pageData.size}-${
                    pageData.page * pageData.size
                } of ${filteredData.length}`
            );
        }
    }, [
        projects.status,
        pageData,
        costRange,
        transactionsRange,
        isAsc,
        sortby,
        filter,
        filterOwner
    ]);
    return (
        <Flex gap={24} vertical>
            <HeaderContainer>
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
                    onClick={() => navigate('/projects/add')}
                >
                    New project
                </Button>
            </HeaderContainer>
            {projects.isLoading && (
                <>
                    <div>loading...</div>
                </>
            )}
            {projects.isError && (
                <>
                    <div>An error has occurred</div>
                    {console.error(projects.error)}
                </>
            )}
            {projects.isSuccess && (
                <div className="px-[24px] max-w-[1600px] w-full mx-auto">
                    {projects.data.length < 1 && (
                        <Flex className="m-auto mt-24" vertical>
                            <img src={noFoundImg} width={250} className="m-auto" />
                            <Title level={2} className="mt-[24px] text-center">
                                Start your journey
                            </Title>
                            <Title level={5} className="text-center text-[16px] mt-[8px]">
                                Create your fist project
                            </Title>
                            <Button
                                className="m-auto mt-[32px]"
                                type="primary"
                                size="large"
                                icon={<PlusSquareOutlined />}
                                onClick={() => navigate('/projects/add')}
                            >
                                New project
                            </Button>
                        </Flex>
                    )}
                    {projects.data.length > 0 && (
                        <>
                            <FilterDashboard
                                costRange={{
                                    ...costRange,
                                    max: projects.data.reduce(
                                        (max, current) =>
                                            current.total_cost > max ? current.total_cost : max,
                                        0
                                    )
                                }}
                                transactionsRange={{
                                    ...transactionsRange,
                                    max: projects.data.reduce(
                                        (max, current) =>
                                            current.total_transactions > max
                                                ? current.total_transactions
                                                : max,
                                        0
                                    )
                                }}
                                owner={filterOwner}
                                onSearch={setFilter}
                                onSortAsc={setAsc}
                                onSortByChange={setSortby}
                                onChangeCost={setCostRange}
                                onChangeTransactions={setTransactionsRange}
                                onSetOwner={setFilterOwner}
                            />
                            {filteredProjects.length > 0 && (
                                <Row
                                    justify="space-between"
                                    className="flex-nowrap gap-[24px] mx-[24px] mt-[8px] mb-[4px]"
                                >
                                    <Col className="max-w-[50%] min-w-[50%] w-full leading-5">
                                        Title:
                                    </Col>
                                    {auth && <Col className="w-full leading-5">Owner:</Col>}
                                    <Col className="w-full text-end leading-5">Transactions:</Col>
                                    <Col className="w-full text-end leading-5">Cost:</Col>
                                </Row>
                            )}
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
                                    <Flex className="m-auto mt-24" vertical>
                                        <img src={noResultsImg} width={250} className="m-auto" />
                                        <Title level={3} className="mt-[24px] text-center">
                                            No results
                                        </Title>
                                        <Title
                                            level={5}
                                            className="max-w-[250px] text-center m-auto"
                                        >
                                            Refine your search or adjust filters to see more
                                            results.
                                        </Title>
                                    </Flex>
                                )}
                            </Flex>
                            {filteredProjects.length > 0 && (
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
                                        hideOnSinglePage={filteredProjects.length < pageData.size}
                                    />
                                </Flex>
                            )}
                        </>
                    )}
                </div>
            )}
        </Flex>
    );
};

export default Dashboard;
