import { useFormik } from 'formik';
import { useGetProviders } from '../../../api/queries';
import { FormikValues } from '../types';
import { makeUrl, toSlug } from '../../../helpers/aiProvider';
import { SetStateAction, useState } from 'react';
import { providerSchema } from '../../../api/formSchemas';
import { Button, Col, Form, Input, Row, Select, Typography } from 'antd';

const { Paragraph } = Typography;

export interface Props {
    EditedProvider: number | null;
    ProvidersList: typeof FormikValues.ai_providers;
    setProvidersList: (list: typeof FormikValues.ai_providers) => void;
    setEditedProvider: (arg: SetStateAction<number | null>) => void;
    setFormShow: (arg: SetStateAction<boolean>) => void;
    slug: string;
}

const ProviderForm: React.FC<Props> = ({
    EditedProvider,
    ProvidersList,
    setProvidersList,
    setEditedProvider,
    setFormShow,
    slug
}) => {
    const providers = useGetProviders();
    const formik = useFormik({
        initialValues:
            EditedProvider != null
                ? {
                      deployment_name: ProvidersList[EditedProvider].deployment_name,
                      slug: ProvidersList[EditedProvider].slug,
                      description: ProvidersList[EditedProvider].description,
                      api_base: ProvidersList[EditedProvider].api_base,
                      provider_name: ProvidersList[EditedProvider].provider_name
                  }
                : {
                      deployment_name: '',
                      slug: '',
                      description: '',
                      api_base: '',
                      provider_name: ''
                  },
        onSubmit: async (values) => {
            const { deployment_name, provider_name, api_base, description } = values;
            if (
                ProvidersList.filter(
                    (e, idx) =>
                        toSlug(e.deployment_name) === toSlug(deployment_name) &&
                        idx != EditedProvider
                ).length > 0
            ) {
                formik.setErrors({ deployment_name: 'Name must be unique' });
            } else {
                formik.setErrors({});
                if (EditedProvider != null) {
                    const newList = ProvidersList.map((el, idx) => {
                        if (idx === EditedProvider)
                            return { ...formik.values, slug: toSlug(deployment_name) };
                        else return el;
                    });
                    setProvidersList(newList);
                    setEditedProvider(null);
                } else
                    setProvidersList([
                        ...ProvidersList,
                        {
                            api_base,
                            slug: toSlug(deployment_name),
                            provider_name,
                            deployment_name,
                            description
                        }
                    ]);
                setFormShow(false);
            }
        },
        validateOnChange: false,
        validationSchema: providerSchema
    });
    const [apiBasePlaceholder, setApiBasePlaceholder] = useState('https://ai-provider.url');
    return (
        <Form
            name="provider_details"
            layout="vertical"
            initialValues={formik.initialValues}
            onSubmitCapture={formik.handleSubmit}
            onFinishFailed={() => console.log(formik.errors)}
            autoComplete="on"
            noValidate={true}
        >
            <Row gutter={12}>
                <Col span={12}>
                    <Form.Item<typeof formik.initialValues>
                        label="AI Providers"
                        name="provider_name"
                        validateStatus={formik.errors.provider_name ? 'error' : ''}
                        help={formik.errors.provider_name}
                        rules={[{ required: true }]}
                    >
                        <Select
                            loading={providers.isLoading}
                            value={formik.values.provider_name}
                            onChange={(val) => {
                                formik.handleChange({
                                    target: {
                                        value: val,
                                        name: 'provider_name'
                                    }
                                });
                                const prov = providers.data?.data.filter(
                                    (el) => el.provider_name === val
                                )[0];
                                setApiBasePlaceholder(
                                    prov?.api_base_placeholder || 'http://your.url'
                                );
                            }}
                            options={[
                                { label: 'Select Provider', value: '' },
                                ...(providers.data?.data.map((el) => ({
                                    label: el.provider_name,
                                    value: el.provider_name
                                })) || [])
                            ]}
                        />
                    </Form.Item>
                </Col>
                <Col span={12}>
                    <Form.Item<typeof formik.initialValues>
                        label="Deployment name"
                        name="deployment_name"
                        validateStatus={formik.errors.deployment_name ? 'error' : ''}
                        help={formik.errors.deployment_name}
                        rules={[{ required: true }]}
                    >
                        <Input
                            name="deployment_name"
                            onChange={formik.handleChange}
                            value={formik.values.deployment_name}
                        />
                    </Form.Item>
                </Col>
            </Row>

            <Form.Item<typeof formik.initialValues>
                label="Api base URL"
                name="api_base"
                validateStatus={formik.errors.api_base ? 'error' : ''}
                help={formik.errors.api_base}
                rules={[{ required: true }]}
            >
                <Input
                    name="api_base"
                    onChange={formik.handleChange}
                    value={formik.values.api_base}
                    placeholder={apiBasePlaceholder}
                />
            </Form.Item>
            <Paragraph className="text-center !mb-0">Proxy URL</Paragraph>
            <Paragraph className="font-medium text-base text-center" copyable>
                {makeUrl(slug, formik.values.deployment_name)}
            </Paragraph>
            <Button type="primary" ghost htmlType="submit" block>
                {EditedProvider != undefined ? 'Update AI Provider' : 'Add AI Provider'}
            </Button>
        </Form>
    );
};

export default ProviderForm;
