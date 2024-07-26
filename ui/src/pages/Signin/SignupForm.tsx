import { Alert, Button, Flex, Form, Input, Typography } from 'antd';
import { useFormik } from 'formik';
import { useContext, useState } from 'react';
import { useAddUser } from '../../api/queries';
import { registerSchema } from '../../api/formSchemas';
import { Context } from '../../context/Context';
const { Paragraph, Link } = Typography;
const SignupForm: React.FC<{ onOk: () => void }> = ({ onOk }) => {
    const register = useAddUser();
    const { notification } = useContext(Context);
    const [errorMessage, setErrorMessage] = useState('');
    const formik = useFormik({
        initialValues: {
            email: '',
            given_name: '',
            family_name: '',
            password: '',
            repeated_password: ''
        },
        onSubmit: (values) => {
            register.mutateAsync(
                {
                    data: {
                        email: values.email,
                        given_name: values.given_name,
                        family_name: values.family_name,
                        password: values.password,
                        repeated_password: values.repeated_password
                    }
                },
                {
                    onError: (err) => {
                        setErrorMessage(err.response?.data?.detail || '');
                    },
                    onSuccess: () => {
                        notification?.success({
                            message: 'Registered successfully!',
                            description: 'Check your email to activate your account.',
                            placement: 'top',
                            duration: 15
                        });
                        onOk();
                    }
                }
            );
        },
        validationSchema: registerSchema,
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
            <Flex gap={12}>
                <Form.Item
                    className="mb-[10px]"
                    help={formik.errors.given_name}
                    validateStatus={formik.errors.given_name ? 'error' : ''}
                >
                    <Paragraph className="!m-0 text-Text/colorText">Given name:</Paragraph>
                    <Input
                        name="given_name"
                        autoComplete="given-name"
                        size="large"
                        placeholder=""
                        value={formik.values.given_name}
                        onChange={formik.handleChange}
                    />
                </Form.Item>
                <Form.Item
                    className="mb-[10px]"
                    help={formik.errors.family_name}
                    validateStatus={formik.errors.family_name ? 'error' : ''}
                >
                    <Paragraph className="!m-0 text-Text/colorText">Family name:</Paragraph>
                    <Input
                        name="family_name"
                        autoComplete="family-name"
                        size="large"
                        placeholder=""
                        value={formik.values.family_name}
                        onChange={formik.handleChange}
                    />
                </Form.Item>
            </Flex>
            <Flex gap={12}>
                <Form.Item
                    className="mb-[10px]"
                    help={formik.errors.password}
                    validateStatus={formik.errors.password ? 'error' : ''}
                >
                    <Paragraph className="!m-0 text-Text/colorText">Password:</Paragraph>
                    <Input
                        name="password"
                        autoComplete="password"
                        type="password"
                        size="large"
                        placeholder=""
                        value={formik.values.password}
                        onChange={formik.handleChange}
                    />
                </Form.Item>
                <Form.Item
                    className="mb-[10px]"
                    help={formik.errors.repeated_password}
                    validateStatus={formik.errors.repeated_password ? 'error' : ''}
                >
                    <Paragraph className="!m-0 text-Text/colorText">Repeat password:</Paragraph>
                    <Input
                        name="repeated_password"
                        autoComplete="repeated_password"
                        type="password"
                        size="large"
                        placeholder=""
                        value={formik.values.repeated_password}
                        onChange={formik.handleChange}
                    />
                </Form.Item>
            </Flex>
            {errorMessage && <Alert message={errorMessage} type="error" showIcon />}
            <Button type="primary" size="large" className="mt-4" block htmlType="submit">
                Submit
            </Button>
            <Link onClick={onOk}>Already have an account? </Link>
        </Form>
    );
};

export default SignupForm;
