import {
    Button,
    Collapse,
    CollapseProps,
    Divider,
    Flex,
    Form,
    Input,
    Typography,
    theme
} from 'antd';
import { FormikProps } from 'formik';
import { FormikValuesTemplate } from '../types';
import { SetStateAction, useState } from 'react';
import { makeUrl, toSlug } from '../../../helpers/aiProvider';
import { DeleteOutlined, DownOutlined, PlusSquareOutlined } from '@ant-design/icons';
import ProviderEditableElement from './ProvidersEditableElement';
import ProviderSelect from './ProviderSelect';
import { CollapsibleType } from 'antd/es/collapse/CollapsePanel';

const { Title, Paragraph } = Typography;

interface Props {
    formik: FormikProps<(typeof FormikValuesTemplate.ai_providers)[0]>;
    projectDetails: typeof FormikValuesTemplate;
    setProjectDetails: (args: SetStateAction<typeof FormikValuesTemplate>) => void;
}

const ProviderDetails: React.FC<Props> = ({ formik, setProjectDetails, projectDetails }) => {
    const { token } = theme.useToken();
    const [collapseTrigger, setcollapseTrigger] = useState<CollapsibleType>('header');
    const items: CollapseProps['items'] = projectDetails.ai_providers.map((el, item_id) => ({
        key: item_id,
        label: (
            <Flex justify="space-between">
                <Title level={2} className="h5 m-0 lh-0">
                    {el.deployment_name}
                </Title>
                <Flex gap={12}>
                    <Button
                        icon={<DeleteOutlined />}
                        size="small"
                        onClick={() => {
                            const newAiProviders = projectDetails.ai_providers.filter(
                                (_el, id) => id !== item_id
                            );
                            setProjectDetails((old) => ({ ...old, ai_providers: newAiProviders }));
                        }}
                        type="text"
                        onMouseEnter={() => setcollapseTrigger('icon')}
                        onMouseLeave={() => setcollapseTrigger('header')}
                    />
                    <Divider type="vertical" className="h-full m-0" />
                </Flex>
            </Flex>
        ),
        style: {
            background: token.colorBgContainer,
            // @ts-expect-error token.Collapse.colorBorder is correctly defined in /ui/src/theme-light.tsx
            border: `1px solid ${token.Collapse.colorBorder}`,
            borderRadius: '8px'
        },
        children: (
            <ProviderEditableElement
                initialValues={el}
                onSubmit={(values) =>
                    setProjectDetails((old) => {
                        const newAiProviders = old.ai_providers.map((el, id) => {
                            if (id === item_id)
                                return { ...values, slug: toSlug(values.deployment_name) };
                            else return el;
                        });
                        return {
                            ...old,
                            ai_providers: newAiProviders
                        };
                    })
                }
                slugForProxy={projectDetails.slug}
                formId={'projectForm_providerEdit' + item_id}
            />
        )
    }));
    return (
        <Flex gap={12} vertical>
            {projectDetails.ai_providers.length > 0 && (
                <Collapse
                    accordion
                    collapsible={collapseTrigger}
                    defaultActiveKey={[]}
                    style={{
                        background: token.Layout?.bodyBg,
                        border: 'none',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 12,
                        padding: 0
                    }}
                    expandIcon={({ isActive }) => (
                        <DownOutlined
                            className="my-auto !text-[14px]"
                            rotate={isActive ? 180 : 0}
                        />
                    )}
                    expandIconPosition="end"
                    items={items}
                />
            )}
            <div className="bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px] divide-y divide-solid divide-Border/colorBorderSecondary">
                <Title level={2} className="h5 m-0 px-[24px] py-[16px]">
                    Project details
                </Title>
                <Form
                    name="projectForm_providers"
                    className="px-[24px] py-[16px] border-0"
                    id="projectForm_providers"
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
                            Provide a short uniqe name to identify your deployment from the AI
                            provider. It will be a part of the proxy URL.
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
                            value={makeUrl(projectDetails.slug, formik.values.deployment_name)}
                            size="large"
                            onChange={formik.handleChange}
                        />
                    </Form.Item>
                </Form>
            </div>
            <Button
                className="me-auto mb-[12px]"
                type="dashed"
                icon={<PlusSquareOutlined />}
                htmlType="submit"
                form="projectForm_providers"
            >
                Add{projectDetails.ai_providers.length > 0 ? ' next' : ''} AI Provider
            </Button>
        </Flex>
    );
};
export default ProviderDetails;
