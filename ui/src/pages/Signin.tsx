import { useFormik } from 'formik';
import { SetStateAction } from 'react';
import { checkLogin } from '../storage/login';
import Logo from '../assets/logo/symbol-teal.svg';
import { Button, Flex, Form, Input, Space, Typography } from 'antd';

const { Title, Paragraph } = Typography;
const Signin: React.FC<{ setLoginState: (arg: SetStateAction<boolean>) => void }> = ({
    setLoginState
}) => {
    const formik = useFormik({
        initialValues: {
            email: '',
            password: ''
        },
        onSubmit: () => {
            localStorage.setItem('login', 'true');
            setLoginState(checkLogin());
        }
    });
    return (
        <Flex justify="center" align="center" className="h-screen">
            <Space direction="vertical" className="signin text-center">
                <Title level={1} className="!m-0">
                    Welcome to Ermlab
                </Title>
                <Title level={2} className="!m-0">
                    Log in to continue
                </Title>
                <Form
                    layout="vertical"
                    onSubmitCapture={formik.handleSubmit}
                    autoComplete="on"
                    noValidate={true}
                >
                    <Form.Item label="Email" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item label="Password" rules={[{ required: true }]}>
                        <Input.Password />
                    </Form.Item>
                    <Button type="primary" htmlType="submit" block>
                        Log In
                    </Button>
                </Form>
                <Space direction="vertical" className="mt-5">
                    <img className="logo" src={Logo} />
                    <Paragraph className="font-bold">Prompt Sail</Paragraph>
                </Space>
            </Space>
        </Flex>
    );
};

export default Signin;
