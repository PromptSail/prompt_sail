import { SetStateAction, useEffect, useState } from 'react';
import { checkLogin } from '../../storage/login';
import Logo from '../../assets/logo/symbol-teal.svg';
import { Flex, Space, Typography } from 'antd';
import GoogleBtn from './GoogleBtn';
import AzureBtn from './AzureBtn';
import api from '../../api/api';
import { GoogleOAuthProvider } from '@react-oauth/google';

const { Title, Paragraph } = Typography;
const Signin: React.FC<{ setLoginState: (arg: SetStateAction<boolean>) => void }> = ({
    setLoginState
}) => {
    const [token, setToken] = useState<null | string>(null);
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
    return (
        <Flex justify="center" align="center" className="h-screen">
            <Space direction="vertical" className="signin text-center">
                <Title level={1} className="!m-0">
                    Welcome to Ermlab
                </Title>
                <Title level={2} className="!m-0">
                    Log in to continue
                </Title>
                <GoogleOAuthProvider clientId={SSO_GOOGLE_ID}>
                    <GoogleBtn onOk={setToken} />
                </GoogleOAuthProvider>
                <AzureBtn onOk={setToken} />
                <Space direction="vertical" className="mt-5">
                    <img className="logo" src={Logo} />
                    <Paragraph className="font-bold">Prompt Sail</Paragraph>
                </Space>
                <p>{token}</p>
            </Space>
        </Flex>
    );
};

export default Signin;
