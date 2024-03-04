import { Link } from 'react-router-dom';
import iconSrc from '../../../assets/icons/box-arrow-up-right.svg';
import { ReactSVG } from 'react-svg';
import { Badge, Flex, Space, Table } from 'antd';
import { TagsContainer } from '../../../helpers/dataContainer';
import { ArrowRightOutlined } from '@ant-design/icons';
import { Dispatch, SetStateAction, useEffect, useState } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllTransactions } from '../../../api/queries';

interface Props {
    filters: TransactionsFilters;
    setFilters: Dispatch<SetStateAction<TransactionsFilters>>;
}
interface DataType {
    key: React.Key;
    time: string;
    latency: string;
    messages: React.ReactNode;
    status: React.ReactNode;
    project: React.ReactNode;
    aiProvider: string;
    model: string;
    tags: React.ReactNode;
    cost: string;
    usage: React.ReactNode;
    more: React.ReactNode;
}

const TransactionsTable: React.FC<Props> = ({ filters, setFilters }) => {
    const transactions = useGetAllTransactions(filters);
    const [isLoading, setLoading] = useState(true);
    const [tableData, setTableData] = useState<{
        items: DataType[];
        page_index: number;
        page_size: number;
        total_elements: number;
    }>({
        items: [],
        page_index: 1,
        page_size: 10,
        total_elements: 0
    });
    const columns = [
        {
            title: 'Time',
            dataIndex: 'time',
            key: 'time',
            width: 175
        },
        {
            title: 'Latency',
            dataIndex: 'latency',
            key: 'latency',
            width: 90
        },
        {
            title: 'Messages',
            dataIndex: 'messages',
            key: 'messages',
            width: 250
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            width: 100
        },
        {
            title: 'Project',
            dataIndex: 'project',
            key: 'project',
            width: 200
        },
        {
            title: 'AI provider',
            dataIndex: 'aiProvider',
            key: 'aiProvider',
            width: 200
        },
        {
            title: 'Model',
            dataIndex: 'model',
            key: 'model',
            width: 200
        },
        {
            title: 'Tags',
            dataIndex: 'tags',
            key: 'tags',
            width: 215
        },
        {
            title: 'Cost',
            dataIndex: 'cost',
            key: 'cost',
            width: 100
        },
        {
            title: 'Usage',
            dataIndex: 'usage',
            key: 'usage',
            width: 150
        },
        {
            title: 'More',
            dataIndex: 'more',
            key: 'more',
            width: 100
        }
    ];
    useEffect(() => {
        if (transactions.isError) {
            console.error(transactions.error);
            alert(`${transactions.error.code}: ${transactions.error.message}`);
        }
        if (transactions.isLoading) {
            setLoading(true);
        }
        if (transactions.isSuccess) {
            setTableData(() => {
                const data = transactions.data.data;
                return {
                    items: data.items.map((tr) => ({
                        key: tr.id,
                        time: new Date(tr.request_time + 'Z')
                            .toLocaleString('pl-PL')
                            .padStart(20, '0'),
                        latency: '2.00s',
                        messages: (
                            <Flex vertical>
                                <div>
                                    <b>Input:</b> {tr.prompt}
                                </div>
                                <div>
                                    <b>Output: </b>{' '}
                                    {tr.message
                                        ? tr.message?.length > 25
                                            ? tr.message?.substring(0, 23) + '...'
                                            : tr.message
                                        : tr.error_message}
                                </div>
                            </Flex>
                        ),
                        status: <Badge status="success" text={tr.status_code} />,
                        project: <Link to={`/projects/${tr.project_id}`}>{tr.project_name}</Link>,
                        aiProvider: 'OpenAI',
                        model: tr.model,
                        tags: <TagsContainer tags={tr.tags} />,
                        cost: '$ 0.02',
                        usage: (
                            <Space>
                                12 <ArrowRightOutlined /> 34 (Σ 46)
                            </Space>
                        ),
                        more: (
                            <Link
                                className="link"
                                target="_blank"
                                id={tr.id}
                                to={`/transactions/${tr.id}`}
                            >
                                <span>Details</span>&nbsp;
                                <ReactSVG src={iconSrc} />
                            </Link>
                        )
                    })),
                    page_index: data.page_index,
                    page_size: data.page_size,
                    total_elements: data.total_elements
                };
            });
            setLoading(false);
        }
    }, [transactions.status]);
    return (
        <Table
            dataSource={tableData.items}
            columns={columns}
            loading={isLoading}
            pagination={{
                position: ['topRight', 'bottomRight'],
                onChange: (page) => {
                    setFilters((old) => ({ ...old, page: `${page}` }));
                },
                onShowSizeChange: (_, size) => {
                    setFilters((old) => ({ ...old, page_size: `${size}` }));
                },
                defaultCurrent: tableData.page_index,
                showSizeChanger: true,
                pageSize: tableData.page_size,
                pageSizeOptions: [5, 10, 20, 50]
            }}
            scroll={{ y: 400 }}
        />
    );
};

export default TransactionsTable;
