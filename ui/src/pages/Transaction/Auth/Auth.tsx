import { useState } from 'react';
import GoogleBtn from './GoogleBtn';
import AzureBtn from './AzureBtn';
import { useGoogleLogin } from '@react-oauth/google';

import MyCustomButton from './MyCustomButton';
import { Flex } from 'antd';

const Auth = () => {
    const [response, setResponse] = useState('');
    const login = useGoogleLogin({
        onSuccess: (codeResponse) =>
            setResponse(JSON.stringify({ response: codeResponse }, null, 4)),
        flow: 'auth-code'
    });

    return (
        <>
            <p># 1</p>
            <Flex>
                <GoogleBtn setResponse={setResponse} />
                <AzureBtn setResponse={setResponse} />
            </Flex>
            <p># 2</p>
            <Flex>
                <MyCustomButton onClick={() => login()}>Sign in with Google 🚀</MyCustomButton>
            </Flex>
            <pre>{response}</pre>
        </>
    );
};

export default Auth;
