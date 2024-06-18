import { Form, Input, Select, Tag, Typography } from 'antd';
import { FormikProps, FormikProvider } from 'formik';
import { toSlug } from '../../helpers/aiProvider';
import { useContext, useState } from 'react';
import { FormikValuesTemplate } from './types';
import UserSelect from './UserSelect';
import { Context } from '../../context/Context';

const { Title, Paragraph, Text } = Typography;

interface Props {
    formik: FormikProps<typeof FormikValuesTemplate>;
}

const ProjectDetails: React.FC<Props> = ({ formik }) => {
    const config = useContext(Context).config;
    const [isSlugGenerated, setSlugGenerate] = useState(true);
    return (
        <div className="bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px] divide-y divide-solid divide-Border/colorBorderSecondary">
            <Title level={2} className="h5 m-0 px-[24px] py-[16px]">
                Project details
            </Title>
            <FormikProvider value={formik}>
                <Form
                    name="projectForm_details"
                    className="px-[24px] py-[16px] border-0"
                    id="projectForm_details"
                    layout="vertical"
                    onSubmitCapture={formik.handleSubmit}
                    onFinishFailed={() => console.log(formik.errors)}
                    autoComplete="on"
                    noValidate={true}
                >
                    <Form.Item<typeof FormikValuesTemplate>
                        rules={[{ required: true }]}
                        className="mb-[10px]"
                    >
                        <Paragraph className="!m-0 text-Text/colorText">Owner:</Paragraph>
                        <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                            You have been assigned automatically as owner.{' '}
                            {config?.authorization
                                ? 'However, you can change it at any time'
                                : 'However, you cannot change it when authorization is disabled'}
                        </Paragraph>
                        <UserSelect className="max-w-[50%]" />
                    </Form.Item>
                    <Form.Item<typeof FormikValuesTemplate>
                        rules={[{ required: true }]}
                        help={formik.errors.name}
                        validateStatus={formik.errors.name ? 'error' : ''}
                        className="mb-[10px]"
                    >
                        <Paragraph className="!m-0 text-Text/colorText">Name:</Paragraph>
                        <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                            Give a unique name for your project.
                        </Paragraph>
                        <Input
                            name="name"
                            className="max-w-[50%]"
                            value={formik.values.name}
                            size="large"
                            showCount
                            maxLength={50}
                            placeholder="Enter name"
                            onKeyUp={(e) => {
                                const val = e.currentTarget.value;
                                if (isSlugGenerated)
                                    formik.setValues((old) => ({
                                        ...old,
                                        slug: toSlug(val)
                                    }));
                            }}
                            onChange={formik.handleChange}
                        />
                    </Form.Item>
                    <Form.Item<typeof FormikValuesTemplate>
                        help={formik.errors.slug}
                        validateStatus={formik.errors.slug ? 'error' : ''}
                        className="mb-[10px]"
                    >
                        <Paragraph className="!m-0 text-Text/colorText">Slug:</Paragraph>
                        <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                            A slug used to identify project is unique and utilized as a part of the
                            proxy URL
                        </Paragraph>
                        <Input
                            name="slug"
                            className="max-w-[50%]"
                            size="large"
                            placeholder="Enter slug"
                            onKeyDown={() => setSlugGenerate(false)}
                            value={formik.values.slug}
                            onBlur={(e) => {
                                const val = e.currentTarget.value;
                                if (val.length < 1) setSlugGenerate(true);
                                e.currentTarget.value = toSlug(val);
                            }}
                            onChange={formik.handleChange}
                        />
                    </Form.Item>
                    <Form.Item<typeof FormikValuesTemplate>
                        help={formik.errors.description}
                        validateStatus={formik.errors.description ? 'error' : ''}
                        className="mb-[10px]"
                    >
                        <Paragraph className="!m-0 text-Text/colorText">
                            Description:{' '}
                            <Text className="text-Text/colorTextDescription">(optional)</Text>
                        </Paragraph>
                        <Input.TextArea
                            name="description"
                            className="max-w-[50%]"
                            placeholder="Enter description"
                            value={formik.values.description}
                            onChange={formik.handleChange}
                            showCount
                            maxLength={400}
                        />
                    </Form.Item>
                    <Form.Item<typeof FormikValuesTemplate>
                        validateStatus={formik.errors.tags ? 'error' : ''}
                        help={formik.errors.tags}
                        className="mb-[10px]"
                    >
                        <Paragraph className="!m-0 text-Text/colorText">
                            Tags: <Text className="text-Text/colorTextDescription">(optional)</Text>
                        </Paragraph>
                        <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                            Add tags to easily search and categorize the project
                        </Paragraph>
                        <Select
                            mode="tags"
                            className="max-w-[50%]"
                            allowClear
                            value={formik.values.tags}
                            tagRender={({ value, closable, onClose }) => {
                                return (
                                    <Tag closable={closable} onClose={onClose}>
                                        {value}
                                    </Tag>
                                );
                            }}
                            onChange={(val) => {
                                formik.handleChange({
                                    target: {
                                        value: val,
                                        name: 'tags'
                                    }
                                });
                            }}
                            options={[
                                {
                                    value: 'research'
                                },
                                {
                                    value: 'experiment'
                                },
                                {
                                    value: 'internal'
                                },
                                {
                                    value: 'education'
                                },
                                {
                                    value: 'finance'
                                },
                                {
                                    value: 'testing'
                                }
                            ]}
                        />
                    </Form.Item>
                </Form>
            </FormikProvider>
        </div>
    );
};
export default ProjectDetails;
