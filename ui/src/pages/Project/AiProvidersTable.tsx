import { Table, Typography } from 'antd';
import { getProjectResponse } from '../../api/interfaces';
import { useEffect, useState } from 'react';
import { makeUrl } from '../../helpers/aiProvider';
const { Text } = Typography;

interface Props {
    providers: getProjectResponse['ai_providers'];
    slug: string;
}
interface DataType {
    key: string;
    provider: string;
    deploymentName: string;
    proxyUrl: string | React.ReactNode;
    apiBaseUrl: string;
}

const AiProvidersTable: React.FC<Props> = ({ providers, slug }) => {
    const [isLoading, setLoading] = useState(true);
    const [tableData, setTableData] = useState<DataType[]>([]);

    useEffect(() => {
        setTableData(
            providers.map((el, id) => ({
                key: `${slug + el.deployment_name + id}`,
                provider: el.provider_name,
                deploymentName: el.deployment_name,
                proxyUrl: <Text copyable>{makeUrl(slug, el.deployment_name)}</Text>,
                apiBaseUrl: el.api_base
            }))
        );
        setLoading(false);
    }, []);
    const columns = [
        {
            title: 'Provider',
            dataIndex: 'provider',
            key: 'provider'
        },
        {
            title: 'Deployment name',
            dataIndex: 'deploymentName',
            key: 'deploymentName'
        },
        {
            title: 'Proxy url',
            dataIndex: 'proxyUrl',
            key: 'proxyUrl'
        },
        {
            title: 'Api base url',
            dataIndex: 'apiBaseUrl',
            key: 'apiBaseUrl'
        }
    ];
    return (
        <Table
            loading={isLoading}
            dataSource={tableData}
            columns={columns}
            pagination={false}
            size="small"
        />
    );
};
export default AiProvidersTable;
