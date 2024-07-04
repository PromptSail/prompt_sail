import { RocketOutlined } from '@ant-design/icons';
import { Button, Flex, Typography } from 'antd';
import lighthouse from '../../assets/illustration-lighthouse.svg';
import { useNavigate } from 'react-router-dom';
const { Title, Text } = Typography;
const Page404: React.FC = () => {
    const navigate = useNavigate();
    return (
        <Flex justify="center" align="center" vertical className="mt-[200px]">
            <img src={lighthouse} alt="lighthouse" />
            <Title level={1} className="h2">
                The page you're looking for is lost at sea
            </Title>
            <Text className="mt-1">
                Make sure the address is correct. If the issue persists contact us.
            </Text>
            <Button
                type="primary"
                icon={<RocketOutlined />}
                className="mt-6"
                onClick={() => navigate('/')}
            >
                Go to projects
            </Button>
        </Flex>
    );
};
export default Page404;
