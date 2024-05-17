import { SetStateAction, useEffect, useState } from 'react';
import { checkLogin } from '../../storage/login';
import Logo from '../../assets/logo/symbol-teal.svg';
import { Button, Flex, Space, Spin, Typography } from 'antd';
import GoogleBtn from './GoogleBtn';
import AzureBtn from './AzureBtn';
import api from '../../api/api';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { useGetConfig } from '../../api/queries';

const { Title, Paragraph } = Typography;
const Signin: React.FC<{ setLoginState: (arg: SetStateAction<boolean>) => void }> = ({
    setLoginState
}) => {
    const [token, setToken] = useState<null | string>(null);
    const config = useGetConfig();
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
            <Flex justify="center" align="center" className="h-screen">
                <Space direction="vertical" className="signin text-center">
                    <Title level={1} className="!m-0">
                        Welcome to {organization}
                    </Title>
                    {!authorization && (
                        <Button type="primary" onClick={() => setToken(`AUTH: ${authorization}`)}>
                            Click to continue
                        </Button>
                    )}
                    {authorization && (
                        <>
                            <Title level={2} className="!m-0">
                                Log in to continue
                            </Title>
                            {google_auth && (
                                <GoogleOAuthProvider clientId={SSO_GOOGLE_ID}>
                                    <GoogleBtn onOk={setToken} />
                                </GoogleOAuthProvider>
                            )}
                            {azure_auth && <AzureBtn onOk={setToken} />}
                        </>
                    )}
                    <Space direction="vertical" className="mt-5">
                        <img className="logo" src={Logo} />
                        <Paragraph className="font-bold">Prompt Sail</Paragraph>
                    </Space>
                </Space>
            </Flex>
        );
    }
};

export default Signin;
