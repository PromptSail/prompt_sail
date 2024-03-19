import { Link, useNavigate, useParams } from 'react-router-dom';
import { useGetTransaction } from '../../api/queries';
import {
    Badge,
    Descriptions,
    DescriptionsProps,
    Flex,
    Space,
    Tabs,
    TabsProps,
    Tooltip,
    Typography
} from 'antd';
import BasicInfo from './BasicInfo';
import Details from './Details';
import { transactionTabOnLoad } from '../../storage/transactionsDetails';
import { TagsContainer } from '../../helpers/dataContainer';
import { ArrowRightOutlined } from '@ant-design/icons';
import Container from '../Project/Container';
const { Title } = Typography;

const Transaction: React.FC = () => {
    const params = useParams();
    const navigate = useNavigate();
    const transaction = useGetTransaction(params.transactionId || '');
    const onChange = (key: string) => {
        localStorage.setItem('transactionDetailsTab', key);
    };
    const toLocalDate = (date: string) => {
        const local = new Date(date + 'Z');
        return `${local.toLocaleDateString()} ${local.toLocaleTimeString()}`;
    };
    if (transaction)
        if (transaction.isLoading)
            return (
                <>
                    <div>loading...</div>
                </>
            );
    if (transaction.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transaction.error)}
                {navigate('/')}
            </>
        );
    if (transaction.isSuccess) {
        const data = transaction.data.data;
        const descItems: DescriptionsProps['items'] = [
            {
                label: 'Project',
                children: <Link to={`/projects/${data.project_id}`}>{data.project_name}</Link>
            },
            {
                label: 'Model',
                children: data.model
            },
            {
                label: 'Cost',
                children: `$ ${data.total_cost.toFixed(4)}`
            },
            {
                label: 'Api base',
                children: data.request.url,
                span: 3
            },
            {
                label: 'Request time',
                children: toLocalDate(data.request_time)
            },
            {
                label: 'Response time',
                children: toLocalDate(data.response_time)
            },
            {
                label: (
                    <Tooltip placement="top" title="Tokens per second">
                        Speed
                    </Tooltip>
                ),
                children: data.generation_speed.toFixed(3)
            },
            {
                label: 'Response status',
                children: <Badge status="success" text={data.status_code} />
            },
            {
                label: 'Tags',
                children: <TagsContainer tags={data.tags} />
            },
            {
                label: 'Tokens',
                children: (
                    <span>
                        {data.input_tokens} <ArrowRightOutlined /> {data.output_tokens} (Σ{' '}
                        {data.response.content.usage.total_tokens})
                    </span>
                )
            }
        ];
        const items: TabsProps['items'] = [
            {
                key: 'basic',
                label: 'Basic',
                children: <BasicInfo data={data} />
            },
            {
                key: 'details',
                label: 'Details',
                children: <Details data={data} />
            }
        ];
        return (
            <Space direction="vertical">
                <Flex align="center" justify="space-between">
                    <Title style={{ margin: 5 }}>Transaction {data.id}</Title>
                </Flex>
                <Container header={''}>
                    <Descriptions items={descItems} />
                </Container>
                <Tabs defaultActiveKey={transactionTabOnLoad()} items={items} onChange={onChange} />
            </Space>
        );
    }
};

export default Transaction;
