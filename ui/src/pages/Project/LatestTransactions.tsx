import { Badge, Flex, Table, Tag, Tooltip } from 'antd';
import { Link } from 'react-router-dom';
import { TagsContainer } from '../../helpers/dataContainer';
import { useEffect, useState } from 'react';
import { DataType, columns } from '../../components/tables/columns';
import { useGetAllTransactions } from '../../api/queries';
import { ArrowRightOutlined } from '@ant-design/icons';

interface Props {
    projectId: string;
}

const LatestTransactions: React.FC<Props> = ({ projectId }) => {
    const transactions = useGetAllTransactions({
        project_id: projectId,
        page_size: '5'
    });
    const [isLoading, setLoading] = useState(false);
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
                                        <Tag color="geekblue" className="m-0">
                                            {tr.id.length > 10
                                                ? tr.id.substring(0, 10) + '...'
                                                : tr.id}
                                        </Tag>
                                    </Tooltip>
                                </Link>
                            ),
                            time: new Date(tr.request_time + 'Z')
                                .toLocaleString('pl-PL')
                                .padStart(20, '0'),
                            speed: tr.generation_speed.toFixed(3),
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
                            status: <Badge status="success" text={tr.status_code} />,
                            project: (
                                <Link to={`/projects/${tr.project_id}`}>{tr.project_name}</Link>
                            ),
                            aiProvider: tr.provider,
                            model: tr.model,
                            tags: <TagsContainer tags={tr.tags} />,
                            cost: `$ ${tr.total_cost.toFixed(4)}`,
                            tokens: (
                                <span>
                                    {tr.input_tokens} <ArrowRightOutlined /> {tr.output_tokens} (Σ{' '}
                                    {tr.response.content.usage.total_tokens})
                                </span>
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
            columns={columns.map((el) => ({
                ...el,
                sorter: false
            }))}
            pagination={false}
            loading={isLoading}
            size="small"
            scroll={{ y: 400 }}
        />
    );
};
export default LatestTransactions;
