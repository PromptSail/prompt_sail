import { Link } from 'react-router-dom';
import { Badge, Flex, Table, Tag, Tooltip } from 'antd';
import { TagsContainer } from '../../../helpers/dataContainer';
import { ArrowRightOutlined } from '@ant-design/icons';
import { Dispatch, SetStateAction, useEffect, useState } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllTransactions } from '../../../api/queries';
import { DataType, columns } from '../columns';

interface Props {
    filters: TransactionsFilters;
    setFilters: Dispatch<SetStateAction<TransactionsFilters>>;
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
                        id: (
                            <Link
                                className="link"
                                target="_blank"
                                id={tr.id}
                                to={`/transactions/${tr.id}`}
                            >
                                <Tooltip
                                    placement="top"
                                    title={tr.id}
                                    overlayStyle={{ maxWidth: '500px' }}
                                >
                                    <Tag color="geekblue" className="m-0">
                                        {tr.id.length > 10 ? tr.id.substring(0, 10) + '...' : tr.id}
                                    </Tag>
                                </Tooltip>
                            </Link>
                        ),
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
                        aiProvider: tr.provider,
                        model: tr.model,
                        tags: <TagsContainer tags={tr.tags} />,
                        cost: '$ 0.02',
                        tokens: (
                            <span>
                                {tr.response.content.usage.completion_tokens} <ArrowRightOutlined />{' '}
                                {tr.response.content.usage.prompt_tokens} (Σ{' '}
                                {tr.response.content.usage.total_tokens})
                            </span>
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