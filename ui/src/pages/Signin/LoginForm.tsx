import { Alert, Button, Form, Input, Typography } from 'antd';
import { useFormik } from 'formik';
import { useLoginUser } from '../../api/queries';
import { useState } from 'react';
const { Paragraph } = Typography;

const LoginForm: React.FC<{ onOk: (value: string) => void }> = ({ onOk }) => {
    const login = useLoginUser();
    const [errorMessage, setErrorMessage] = useState('');
    const formik = useFormik({
        initialValues: { login: '', password: '' },
        onSubmit: (values) => {
            login.mutateAsync(
                {
                    data: {
                        username: values.login,
                        password: values.password
                    }
                },
                {
                    onError: (err) => {
                        setErrorMessage(err.response?.data?.detail || '');
                    },
                    onSuccess: (data) => {
                        onOk(data.data);
                    }
                }
            );
        }
    });
    return (
        <Form onSubmitCapture={formik.handleSubmit}>
            <Form.Item className="mb-[10px]">
                <Paragraph className="!m-0 text-Text/colorText">Login:</Paragraph>
                <Input
                    name="login"
                    size="large"
                    placeholder=""
                    autoComplete="username"
                    value={formik.values.login}
                    onChange={formik.handleChange}
                />
            </Form.Item>
            <Form.Item className="mb-[10px]">
                <Paragraph className="!m-0 text-Text/colorText">Password:</Paragraph>
                <Input
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    size="large"
                    placeholder=""
                    value={formik.values.password}
                    onChange={formik.handleChange}
                />
            </Form.Item>
            {errorMessage && <Alert message={errorMessage} type="error" showIcon />}
            <Button type="primary" size="large" block htmlType="submit" className="mt-4">
                Login
            </Button>
        </Form>
    );
};
export default LoginForm;
