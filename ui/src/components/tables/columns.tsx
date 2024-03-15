export interface DataType {
    key: React.Key;
    id: React.ReactNode;
    time: string;
    latency: string;
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
        title: 'Tokens',
        dataIndex: 'tokens',
        key: 'tokens',
        width: 150
    }
];
