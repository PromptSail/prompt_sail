import { Link, useNavigate, useParams } from 'react-router-dom';
import { useGetTransaction } from '../../api/queries';
import { Breadcrumb, Flex, Spin, Tabs, Typography } from 'antd';
import HeaderContainer from '../../components/HeaderContainer/HeaderContainer';
import { useState } from 'react';
import TransactionDetails from './TransactionDetails';
import Details from './Details';
import Messages from './Messages';
const { Title } = Typography;

const Transaction: React.FC = () => {
    const params = useParams();
    const navigate = useNavigate();
    const transaction = useGetTransaction(params.transactionId || '');
    const [currentTab, setCurrentTab] = useState('1');
    if (transaction)
        if (transaction.isLoading)
            return (
                <Spin
                    size="large"
                    className="absolute top-1/3 left-1/2 -transtaction-x-1/2 -transtaction-y-1/3"
                />
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
        return (
            <Flex vertical>
                <HeaderContainer height={123.5}>
                    <Flex vertical>
                        <Flex vertical justify="space-between">
                            <Breadcrumb
                                className="ms-1"
                                items={[
                                    {
                                        title: <Link to={'/transactions'}>Transactions</Link>
                                    },
                                    {
                                        title: data.id
                                    }
                                ]}
                            />
                            <Title level={1} className="h4 m-0">
                                {data.id}
                            </Title>
                        </Flex>
                        <Tabs
                            defaultActiveKey={currentTab}
                            className="project-tab"
                            onChange={(activeKey) => setCurrentTab(activeKey)}
                            items={[
                                {
                                    key: '1',
                                    label: 'Overview'
                                },
                                {
                                    key: '2',
                                    label: 'Messages'
                                },
                                {
                                    key: '3',
                                    label: 'JSON files'
                                }
                            ]}
                        />
                    </Flex>
                </HeaderContainer>
                <div className="px-[24px] pt-[24px] max-w-[1600px] w-full mx-auto">
                    <Flex className="m-auto" vertical gap={12}>
                        <></>
                        {currentTab == '1' && <TransactionDetails data={data} />}
                        {currentTab == '2' && <Messages data={data} />}
                        {currentTab == '3' && <Details data={data} />}
                    </Flex>
                </div>
            </Flex>
        );
    }
};

export default Transaction;
