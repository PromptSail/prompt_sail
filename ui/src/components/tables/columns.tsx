import { ArrowRightOutlined } from '@ant-design/icons';
import { Tooltip } from 'antd';

export interface DataType {
    key: React.Key;
    id: React.ReactNode;
    time: string;
    speed: string;
    messages: React.ReactNode;
    status: React.ReactNode;
    project: React.ReactNode;
    aiProvider: string;
    model: string;
    tags: React.ReactNode;
    cost: string;
    tokens: React.ReactNode;
}

export const columns = [
    {
        title: 'ID',
        dataIndex: 'id',
        key: 'id',
        width: 120
    },
    {
        title: 'Time',
        dataIndex: 'time',
        key: 'time',
        sorter: true,
        apiCol: 'request_time',
        width: 175
    },
    {
        title: (
            <Tooltip placement="top" title="Tokens per second">
                Speed
            </Tooltip>
        ),
        dataIndex: 'speed',
        key: 'speed',
        sorter: true,
        apiCol: 'generation_speed',
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
        sorter: true,
        apiCol: 'status_code',
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
        sorter: true,
        apiCol: 'provider',
        width: 200
    },
    {
        title: 'Model',
        dataIndex: 'model',
        key: 'model',
        sorter: true,
        apiCol: 'model',
        width: 200
    },
    {
        title: 'Tags',
        dataIndex: 'tags',
        key: 'tags',
        sorter: true,
        apiCol: 'tags',
        width: 215
    },
    {
        title: 'Cost',
        dataIndex: 'cost',
        key: 'cost',
        width: 100
    },
    {
        title: (
            <Tooltip
                placement="top"
                title={
                    <span>
                        input <ArrowRightOutlined /> output (Σ total)
                    </span>
                }
            >
                Tokens
            </Tooltip>
        ),
        dataIndex: 'tokens',
        key: 'tokens',
        width: 150
    }
];
