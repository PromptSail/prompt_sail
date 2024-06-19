import { Button, Form, Input, Typography } from 'antd';
import { useFormik } from 'formik';
import { makeUrl } from '../../../helpers/aiProvider';
import { providerSchema } from '../../../api/formSchemas';
import ProviderSelect from './ProviderSelect';
import { FormikValuesTemplate } from '../types';

const { Paragraph } = Typography;

interface Props {
    initialValues: (typeof FormikValuesTemplate.ai_providers)[0];
    onSubmit: (values: (typeof FormikValuesTemplate.ai_providers)[0]) => void;
    slugForProxy: string;
    formId: string;
    showSubmitButton?: boolean;
}

const ProviderEditableElement: React.FC<Props> = ({
    initialValues,
    onSubmit,
    formId,
    slugForProxy,
    showSubmitButton = true
}) => {
    const formik = useFormik({
        initialValues: initialValues,
        onSubmit,
        validationSchema: providerSchema,
        validateOnChange: false
    });
    return (
        <>
            <Form
                name={formId}
                className="border-0"
                id={formId}
                layout="vertical"
                onSubmitCapture={formik.handleSubmit}
                onFinishFailed={() => console.log(formik.errors)}
                autoComplete="on"
                noValidate={true}
            >
                <Form.Item<typeof FormikValuesTemplate>
                    rules={[{ required: true }]}
                    help={formik.errors.provider_name}
                    validateStatus={formik.errors.provider_name ? 'error' : ''}
                    className="mb-[10px]"
                >
                    <Paragraph className="!m-0 text-Text/colorText">AI Provider:</Paragraph>
                    <ProviderSelect
                        className="max-w-[50%]"
                        value={formik.values.provider_name}
                        size="large"
                        onChange={(val) => {
                            formik.handleChange({
                                target: {
                                    value: val,
                                    name: 'provider_name'
                                }
                            });
                        }}
                    />
                </Form.Item>
                <Form.Item<typeof FormikValuesTemplate>
                    rules={[{ required: true }]}
                    help={formik.errors.deployment_name}
                    validateStatus={formik.errors.deployment_name ? 'error' : ''}
                    className="mb-[10px]"
                >
                    <Paragraph className="!m-0 text-Text/colorText">Deployment name:</Paragraph>
                    <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                        Provide a short uniqe name to identify your deployment from the AI provider.
                        It will be a part of the proxy URL.
                    </Paragraph>
                    <Input
                        className="max-w-[50%]"
                        name="deployment_name"
                        value={formik.values.deployment_name}
                        size="large"
                        onChange={formik.handleChange}
                    />
                </Form.Item>
                <Form.Item<typeof FormikValuesTemplate>
                    rules={[{ required: true }]}
                    help={formik.errors.api_base}
                    validateStatus={formik.errors.api_base ? 'error' : ''}
                    className="mb-[10px]"
                >
                    <Paragraph className="!m-0 text-Text/colorText">API Base URL:</Paragraph>
                    <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                        Enter the base URL for the LLM endpoint you want to connect with
                    </Paragraph>
                    <Input
                        className="max-w-[50%]"
                        name="api_base"
                        value={formik.values.api_base}
                        size="large"
                        onChange={formik.handleChange}
                    />
                </Form.Item>
                <Form.Item<typeof FormikValuesTemplate>
                    rules={[{ required: true }]}
                    help={formik.errors.slug}
                    validateStatus={formik.errors.slug ? 'error' : ''}
                    className="mb-[10px]"
                >
                    <Paragraph className="!m-0 text-Text/colorText">API Base URL:</Paragraph>
                    <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                        Enter the base URL for the LLM endpoint you want to connect with
                    </Paragraph>
                    <Input
                        className="max-w-[50%]"
                        disabled
                        value={makeUrl(slugForProxy, formik.values.deployment_name)}
                        size="large"
                        onChange={formik.handleChange}
                    />
                </Form.Item>
            </Form>
            {showSubmitButton && (
                <Button
                    className="me-auto"
                    type="primary"
                    htmlType="submit"
                    form={formId}
                    disabled={(() => {
                        const isValuesNotEdited = Object.keys(initialValues)
                            .filter((el) => el !== 'slug')
                            .map((el) => {
                                const key = el as keyof typeof initialValues;
                                return initialValues[key] === formik.values[key];
                            });
                        return isValuesNotEdited.reduce((a, b) => a && b);
                    })()}
                >
                    Save
                </Button>
            )}
        </>
    );
};

export default ProviderEditableElement;
