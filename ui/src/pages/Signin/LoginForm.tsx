import { Alert, Button, Form, Input, Typography } from 'antd';
import { useFormik } from 'formik';
import { useLoginUser } from '../../api/queries';
import { useState } from 'react';
import { loginSchema } from '../../api/formSchemas';
const { Paragraph, Link } = Typography;

const LoginForm: React.FC<{ onOk: (value: string) => void; onSignup: () => void }> = ({
    onOk,
    onSignup
}) => {
    const login = useLoginUser();
    const [errorMessage, setErrorMessage] = useState('');
    const formik = useFormik({
        initialValues: { email: '', password: '' },
        onSubmit: (values) => {
            login.mutateAsync(
                {
                    data: {
                        email: values.email,
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
                help={formik.errors.email}
                validateStatus={formik.errors.email ? 'error' : ''}
            >
                <Paragraph className="!m-0 text-Text/colorText">Email:</Paragraph>
                <Input
                    name="email"
                    size="large"
                    placeholder=""
                    autoComplete="email"
                    value={formik.values.email}
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
            <Button type="primary" size="large" block htmlType="submit" className="mt-4">
                Sign in
            </Button>
            <Link onClick={onSignup}>Doesn't have an account?</Link>
        </Form>
    );
};
export default LoginForm;