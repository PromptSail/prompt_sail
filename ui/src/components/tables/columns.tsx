export interface DataType {
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

export const columns = [
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
