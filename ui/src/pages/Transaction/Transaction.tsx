import { Link, useParams } from 'react-router-dom';
import { useGetTransaction } from '../../api/queries';
import { Breadcrumb, Flex, Spin, Tabs, Typography } from 'antd';
import HeaderContainer from '../../components/HeaderContainer/HeaderContainer';
import { useState } from 'react';
import Overview from './Overview';
import Messages from './Messages';
import JSONformat from './JSONformat';
import Page404 from '../../components/errorPages/page404';
const { Title } = Typography;

const Transaction: React.FC = () => {
    const params = useParams();
    const transaction = useGetTransaction(params.transactionId || '');
    const [currentTab, setCurrentTab] = useState('1');
    if (transaction)
        if (transaction.isLoading)
            return (
                <div className="w-full h-full relative">
                    <Spin
                        size="large"
                        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                    />
                </div>
            );
    if (transaction.isError) return <Page404 />;
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
                            className="header-tab"
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
                                    label: 'JSON'
                                }
                            ]}
                        />
                    </Flex>
                </HeaderContainer>
                <div className="px-[24px] pt-[24px] max-w-[1600px] w-full mx-auto">
                    <Flex className="m-auto" vertical gap={12}>
                        <></>
                        {currentTab == '1' && <Overview data={data} />}
                        {currentTab == '2' && <Messages data={data} />}
                        {currentTab == '3' && <JSONformat data={data} />}
                    </Flex>
                </div>
            </Flex>
        );
    }
};

export default Transaction;
