import { Form, Input, Typography } from 'antd';
import ProviderSelect from './ProviderSelect';
import { FormikValuesTemplate } from '../types';
import { makeUrl } from '../../../helpers/aiProvider';
import { FormikProps, useFormik } from 'formik';
import { getProjectResponse } from '../../../api/interfaces';
import { providerSchema } from '../../../api/formSchemas';
import { useEffect } from 'react';
const { Paragraph } = Typography;

interface Props {
    // formik: FormikProps<(typeof FormikValuesTemplate.ai_providers)[0]>;
    slug: getProjectResponse['slug'];
    onOk: (values: (typeof FormikValuesTemplate.ai_providers)[0]) => void;
    providers: typeof FormikValuesTemplate.ai_providers;
    formId: string;
    handleFormikInstance?: (
        formik: FormikProps<(typeof FormikValuesTemplate.ai_providers)[0]>
    ) => void;
}
const ProviderForm: React.FC<Props> = ({ slug, providers, onOk, formId, handleFormikInstance }) => {
    const formik = useFormik({
        initialValues: { ...FormikValuesTemplate.ai_providers[0] },
        onSubmit: async (values) => {
            const isProviderNameUniqe =
                providers.filter((e) => e.deployment_name === values.deployment_name).length < 1;
            if (isProviderNameUniqe) {
                onOk(values);
                formik.setValues({
                    ...FormikValuesTemplate.ai_providers[0]
                });
            } else
                formik.setErrors({
                    deployment_name: 'Already exist deployment with this name'
                });
        },
        validationSchema: providerSchema,
        validateOnChange: false
    });
    useEffect(() => {
        if (handleFormikInstance) handleFormikInstance(formik);
        // console.log(formik.values.deployment_name);
    }, [formik]);
    return (
        <Form
            name={formId}
            className="px-[24px] py-[16px] border-0"
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
                    Provide a short uniqe name to identify your deployment from the AI provider. It
                    will be a part of the proxy URL.
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
                    value={makeUrl(slug, formik.values.deployment_name)}
                    size="large"
                    onChange={formik.handleChange}
                />
            </Form.Item>
        </Form>
    );
};

export default ProviderForm;
