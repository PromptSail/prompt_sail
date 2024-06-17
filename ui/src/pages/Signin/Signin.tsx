import { useCallback, useEffect, useState } from 'react';
import { checkLogin } from '../../storage/login';
import Logo from '../../assets/logo/symbol-teal.svg';
import { Button, Divider, Flex, Space, Spin, Typography } from 'antd';
import GoogleBtn from './GoogleBtn';
import AzureBtn from './AzureBtn';
import api from '../../api/api';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { useGetConfig } from '../../api/queries';
import Container from '../../components/Container/Container';
import { ArrowRightOutlined } from '@ant-design/icons';
import { useLogin } from '../../context/LoginContext';

// symbol from ../../assets/logo/symbol-teal-outline.svg
const symbol = (
    <svg fill="none" viewBox="55 5 55 45" xmlns="http://www.w3.org/2000/svg">
        <path
            d="M56 48.999C64.9374 46.2027 71.4229 37.8582 71.4229 27.999C71.4229 18.1398 64.9374 9.79535 56 6.99902H88.4228C100.021 6.99902 109.423 16.4011 109.423 27.999C109.423 39.597 100.021 48.999 88.4228 48.999H56Z"
            strokeWidth=".06"
            stroke="white"
        />
    </svg>
);

const { Title, Paragraph, Text } = Typography;
const Signin: React.FC = () => {
    const [token, setToken] = useState<null | string>(null);
    const config = useGetConfig();
    const [googleBtnWidth, setGoogleBtnWidth] = useState(300);
    const { setLoginState } = useLogin();
    useEffect(() => {
        if (token !== null) {
            localStorage.setItem('PS_TOKEN', token);
            api.whoami()
                .then(() => {
                    setLoginState(checkLogin());
                })
                .catch((err) => {
                    console.error(err);
                });
        }
    }, [token]);
    const setWidth = useCallback((node: HTMLDivElement) => {
        if (node !== null) setGoogleBtnWidth(node.clientWidth);
    }, []);
    if (config.isError)
        return (
            <>
                <div>An error has occurred {config.error.code}</div>
                {console.error(config.error)}
            </>
        );
    if (config.isLoading)
        return (
            <Spin
                size="large"
                className="absolute top-1/2 left-1/2 -transtaction-x-1/2 -transtaction-y-1/2"
            />
        );
    if (config.isSuccess) {
        const { authorization, organization, azure_auth, google_auth } = config.data.data;
        return (
            <Flex justify="center" align="center" className="h-screen m-10">
                <Container classname="w-full h-full max-w-[1200px] max-h-[700px]">
                    <Flex
                        // gap={80}
                        align="center"
                        className="h-full w-[calc(100%-24px)] max-w-[2000px] m-3"
                    >
                        <div className="h-full flex-2">
                            <div className="ms-auto w-full h-full bg-[url('/src/assets/signin.png')] bg-[length:auto_100%] bg-bottom bg-no-repeat rounded-[8px]">
                                <Flex
                                    align="center"
                                    justify="center"
                                    className="w-full h-full p-9 bg-Text/colorTextSecondary rounded-[8px] relative overflow-hidden"
                                >
                                    <div className="w-[350px] absolute left-[5%] -top-[15%]">
                                        {symbol}
                                    </div>
                                    <div className="w-[350px] absolute left-[45%] top-[75%]">
                                        {symbol}
                                    </div>
                                    <Text className="text-[32px] leading-[1.2] font-['Unica_One'] text-white uppercase text-center">
                                        Smooth sailing for your LLM&nbsp;operations
                                    </Text>
                                </Flex>
                            </div>
                        </div>
                        <Flex
                            ref={setWidth}
                            className="signin m-auto min-w-[400px] flex-1 mx-[80px] me-[44px]"
                            gap={48}
                            vertical
                        >
                            <Space direction="horizontal">
                                <img src={Logo} width={30} />
                                <Text className="text-[32px] font-['Unica_One'] uppercase">
                                    Prompt Sail
                                </Text>
                            </Space>
                            <Space direction="vertical">
                                <Title level={1} className="!m-0">
                                    {authorization ? 'Log in' : 'Welcome'} to {organization}
                                </Title>
                                <Paragraph>
                                    Unlock cost control, security, and optimization for your large
                                    language model interactions.
                                </Paragraph>
                            </Space>
                            <Space direction="vertical">
                                {!authorization && (
                                    <Button
                                        type="primary"
                                        block
                                        onClick={() => setToken(`AUTH: ${authorization}`)}
                                        icon={<ArrowRightOutlined />}
                                        iconPosition="end"
                                        size="large"
                                    >
                                        Get started
                                    </Button>
                                )}
                                {authorization && (
                                    <>
                                        {google_auth && (
                                            <GoogleOAuthProvider clientId={SSO_GOOGLE_ID}>
                                                <GoogleBtn onOk={setToken} width={googleBtnWidth} />
                                            </GoogleOAuthProvider>
                                        )}
                                        {google_auth && azure_auth && (
                                            <Divider className="!font-normal !m-0">or</Divider>
                                        )}
                                        {azure_auth && <AzureBtn onOk={setToken} />}
                                    </>
                                )}
                            </Space>
                        </Flex>
                    </Flex>
                </Container>
            </Flex>
        );
    }
};

export default Signin;
