import { getAllTransactionResponse } from '../../../api/interfaces';
import { Link } from 'react-router-dom';
import iconSrc from '../../../assets/icons/box-arrow-up-right.svg';
import { ReactSVG } from 'react-svg';
import { Badge, Flex, Space, Table } from 'antd';
import { TagsContainer } from '../../../helpers/dataContainer';
import { ArrowRightOutlined } from '@ant-design/icons';

interface Props {
    data: getAllTransactionResponse['items'];
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

const TransactionsTable: React.FC<Props> = ({ data }) => {
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
    const tableData: DataType[] = [];
    data.map((tr) =>
        tableData.push({
            key: tr.id,
            time: tr.request_time,
            latency: '2.00s',
            messages: (
                <Flex vertical>
                    <div>
                        <b>Input:</b> {tr.prompt}
                    </div>
                    <div>
                        <b>Output: </b> {tr.message}
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
                <Link className="link" target="_blank" id={tr.id} to={`/transactions/${tr.id}`}>
                    <span>Details</span>&nbsp;
                    <ReactSVG src={iconSrc} />
                </Link>
            )
        })
    );
    return (
        <Table
            dataSource={tableData}
            columns={columns}
            pagination={{
                position: ['topRight', 'bottomRight'],
                showSizeChanger: true,
                defaultPageSize: 5,
                pageSizeOptions: [5, 10, 20, 50],
                total: 50
            }}
            scroll={{ y: 400 }}
        />
    );
};

export default TransactionsTable;
