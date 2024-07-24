import { Alert, Button, Flex, Form, Input, Typography } from 'antd';
import { useFormik } from 'formik';
import { useLoginUser } from '../../api/queries';
import { useState } from 'react';
import { loginSchema } from '../../api/formSchemas';
const { Paragraph } = Typography;

const LoginForm: React.FC<{ onOk: (value: string) => void; onSignup: () => void }> = ({
    onOk,
    onSignup
}) => {
    const login = useLoginUser();
    const [errorMessage, setErrorMessage] = useState('');
    const formik = useFormik({
        initialValues: { username: '', password: '' },
        onSubmit: (values) => {
            login.mutateAsync(
                {
                    data: {
                        username: values.username,
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
        },
        validationSchema: loginSchema,
        validateOnChange: false
    });
    return (
        <Form onSubmitCapture={formik.handleSubmit}>
            <Form.Item
                className="mb-[10px]"
                help={formik.errors.username}
                validateStatus={formik.errors.username ? 'error' : ''}
            >
                <Paragraph className="!m-0 text-Text/colorText">Login:</Paragraph>
                <Input
                    name="username"
                    size="large"
                    placeholder=""
                    autoComplete="username"
                    value={formik.values.username}
                    onChange={formik.handleChange}
                />
            </Form.Item>
            <Form.Item
                className="mb-[10px]"
                help={formik.errors.password}
                validateStatus={formik.errors.password ? 'error' : ''}
            >
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
            <Flex gap={12}>
                <Button type="primary" size="large" block htmlType="submit" className="mt-4">
                    Sign in
                </Button>
                <Button size="large" className="mt-4" onClick={onSignup}>
                    Sign up
                </Button>
            </Flex>
        </Form>
    );
};
export default LoginForm;
