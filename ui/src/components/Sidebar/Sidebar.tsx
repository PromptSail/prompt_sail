import { Button, Flex, Typography } from 'antd';
import Sider from 'antd/es/layout/Sider';
import { SetStateAction } from 'react';
import { useNavigate } from 'react-router-dom';
import { checkLogin } from '../../storage/login';
const { Text } = Typography;

interface Props {
    setLoginState: (arg: SetStateAction<boolean>) => void;
}

const Sidebar: React.FC<Props> = ({ setLoginState }) => {
    const navigate = useNavigate();
    return (
        <Sider
            width={250}
            style={{
                overflow: 'auto',
                height: '100vh',
                position: 'fixed',
                left: 0,
                top: 0,
                bottom: 0
            }}
        >
            <Flex vertical justify="space-between" style={{ height: '100%' }}>
                <Flex className="top" vertical gap={20} style={{ padding: '10px' }}>
                    <Flex className="info" vertical>
                        <Text style={{ color: 'white', fontSize: '1.2em', fontWeight: 'bold' }}>
                            John Doe
                        </Text>
                        <Text style={{ color: '#DDD' }}>JohnDoe@gmail.com</Text>
                    </Flex>
                    <Flex className="buttons" vertical gap={10}>
                        <Button type="primary" onClick={() => navigate('/')} block>
                            Projects
                        </Button>
                        <Button type="primary" onClick={() => navigate('/transactions')} block>
                            Transactions
                        </Button>
                    </Flex>
                </Flex>
                <Flex className="bottom" vertical gap={20} style={{ padding: '10px' }}>
                    <Button
                        ghost
                        onClick={() => {
                            localStorage.removeItem('PS_TOKEN');
                            setLoginState(checkLogin());
                        }}
                    >
                        Log out
                    </Button>
                </Flex>
            </Flex>
        </Sider>
    );
};
export default Sidebar;
