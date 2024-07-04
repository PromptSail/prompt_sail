import { Flex, Layout, Typography } from 'antd';
import lifebuoy from '../../assets/illustration-lifebuoy.svg';
import logo from '../../assets/logo/Logo-teal_white.svg';
const { Title, Text } = Typography;
const Page500: React.FC = () => {
    return (
        <Layout className="h-screen">
            <Layout.Header className="bg-Text/colorTextBase" style={{ padding: '0 24px' }}>
                <img src={logo} alt="Prompt sail" className="h-full py-[20px]" />
            </Layout.Header>
            <Layout>
                <Flex justify="center" align="center" vertical className="mt-[200px]">
                    <img src={lifebuoy} alt="lighthouse" />
                    <Title level={1} className="h2">
                        Prompt Sail is battling a storm
                    </Title>
                    <Text className="mt-1">
                        We are working hard to fix the issue. Please return shortly.
                    </Text>
                </Flex>
            </Layout>
        </Layout>
    );
};
export default Page500;
