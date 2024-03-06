import { useNavigate, useParams } from 'react-router-dom';
import { useGetTransaction } from '../../api/queries';
import { Flex, Space, Tabs, TabsProps, Typography } from 'antd';
import BasicInfo from './BasicInfo';
import Details from './Details';
import { transactionTabOnLoad } from '../../storage/transactionsDetails';
const { Title } = Typography;

const Transaction: React.FC = () => {
    const params = useParams();
    const navigate = useNavigate();
    const transaction = useGetTransaction(params.transactionId || '');
    const onChange = (key: string) => {
        localStorage.setItem('transactionDetailsTab', key);
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
                <Tabs defaultActiveKey={transactionTabOnLoad()} items={items} onChange={onChange} />
            </Space>
        );
    }
};

export default Transaction;
