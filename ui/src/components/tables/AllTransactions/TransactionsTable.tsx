import { Link } from 'react-router-dom';
import { Badge, Flex, Table, Tag, Tooltip } from 'antd';
import { TagsContainer } from '../../../helpers/dataContainer';
import { ArrowRightOutlined } from '@ant-design/icons';
import { SetStateAction, useEffect, useState } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllTransactions } from '../../../api/queries';
import columns, { CustomColumns, DataType } from '../columns';
import * as styles from '../../../styles.json';
import { SorterResult } from 'antd/es/table/interface';

interface Props {
    filters: TransactionsFilters;
    setFilters: (attr: SetStateAction<TransactionsFilters>) => void;
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
                    items: data.items.map((tr) => {
                        const rightMessage = tr.error_message || tr.last_message;
                        return {
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
                                        <Tag
                                            style={{
                                                color: styles.Colors.light['Primary/colorPrimary'],
                                                borderColor:
                                                    styles.Colors.light[
                                                        'Primary/colorPrimaryBorder'
                                                    ],
                                                background:
                                                    styles.Colors.light['Primary/colorPrimaryBg']
                                            }}
                                            className="m-0"
                                        >
                                            {tr.id.length > 10
                                                ? tr.id.substring(0, 17) + '...'
                                                : tr.id}
                                        </Tag>
                                    </Tooltip>
                                </Link>
                            ),
                            time: new Date(tr.request_time + 'Z')
                                .toLocaleString('pl-PL')
                                .padStart(20, '0'),
                            speed:
                                tr.status_code < 300 && tr.generation_speed !== null
                                    ? tr.generation_speed.toFixed(3)
                                    : 'null',
                            messages: (
                                <Flex vertical>
                                    <div>
                                        <b>Input:</b> {tr.prompt}
                                    </div>
                                    <div>
                                        <b>Output: </b>{' '}
                                        {rightMessage.length > 25
                                            ? rightMessage.substring(0, 23) + '...'
                                            : rightMessage}
                                    </div>
                                </Flex>
                            ),
                            status: (
                                <Badge
                                    status={
                                        tr.status_code >= 300
                                            ? tr.status_code >= 400
                                                ? 'error'
                                                : 'warning'
                                            : 'success'
                                    }
                                    text={tr.status_code}
                                />
                            ),
                            project: (
                                <Link to={`/projects/${tr.project_id}`}>{tr.project_name}</Link>
                            ),
                            aiProvider: tr.provider,
                            model: tr.model,
                            tags: <TagsContainer tags={tr.tags} classname="w-full" />,
                            cost:
                                tr.status_code < 300 && tr.total_cost !== null
                                    ? `$ ${tr.total_cost.toFixed(4)}`
                                    : 'null',
                            tokens:
                                tr.status_code < 300 ? (
                                    <span>
                                        {tr.input_tokens} <ArrowRightOutlined /> {tr.output_tokens}{' '}
                                        (Σ {tr.response.content.usage.total_tokens})
                                    </span>
                                ) : (
                                    <span>null</span>
                                )
                        };
                    }),
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
            columns={columns(filters, setFilters)}
            loading={isLoading}
            pagination={{
                position: ['bottomRight'],
                onChange: (page, pageSize) => {
                    if (filters.page !== `${page}`) {
                        setFilters((old) => ({ ...old, page: `${page}` }));
                        // setURLParam({ page: `${page}` });
                    }
                    if (filters.page_size !== `${pageSize}`) {
                        setFilters((old) => ({ ...old, page_size: `${pageSize}` }));
                        // setURLParam({ page_size: `${pageSize}` });
                    }
                },
                total: tableData.total_elements,
                current: tableData.page_index,
                showSizeChanger: true,
                pageSize: tableData.page_size,
                pageSizeOptions: [5, 10, 20, 50]
            }}
            onChange={(_pagination, _filters, sorter) => {
                const sortData = sorter as SorterResult<DataType>;
                setFilters((old) => ({
                    ...old,
                    sort_field: sortData.column ? (sortData.column as CustomColumns).apiCol : '',
                    sort_type: sortData.order === 'ascend' ? 'asc' : ''
                }));
            }}
            scroll={{ y: 'true' }} // y: 'true' is a magic value that makes the table scrollbar styles work
            className="transactions-table"
        />
    );
};

export default TransactionsTable;
