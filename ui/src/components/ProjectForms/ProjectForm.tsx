import { useFormik } from 'formik';
import { useEffect, useState } from 'react';
import ProviderFormAndList from './ProviderFormAndList/ProviderFormAndList';
import { projectSchema } from '../../api/formSchemas';
import { useGetAllProjects } from '../../api/queries';
import { toSlug } from '../../helpers/aiProvider';
import { Col, Form, Input, Row, Select, Tag } from 'antd';
import Container from '../../pages/Project/Container';
import { FormikValues } from './types';

interface Props {
    submitFunc: (values: typeof FormikValues) => Promise<void>;
    formId: string;
    projectId?: string;
}

const ProjectForm: React.FC<Props> = ({ submitFunc, formId, projectId }) => {
    const projects = useGetAllProjects();
    const [isSlugGenerated, setSlugGenerate] = useState(true);
    const formik = useFormik({
        initialValues: {
            ...FormikValues,
            ai_providers: [] as typeof FormikValues.ai_providers
        },
        onSubmit: async (values) => {
            if (projects.isSuccess) {
                const noEditedProjects = projects.data.filter((e) => e.id !== (projectId || ''));
                const isNameUnique =
                    noEditedProjects.filter((e) => e.name === values.name).length < 1;
                const isSlugUnique =
                    noEditedProjects.filter((e) => e.slug === toSlug(values.slug)).length < 1;
                if (isNameUnique && isSlugUnique)
                    submitFunc({
                        ...values,
                        slug: toSlug(values.slug)
                    });
                else {
                    if (!isNameUnique)
                        formik.setErrors({
                            ...formik.errors,
                            name: 'There is already a project with this name in your organisation'
                        });
                    if (!isSlugUnique)
                        formik.setErrors({
                            ...formik.errors,
                            slug: 'In your organization this slug is already taken'
                        });
                }
            }
        },
        validationSchema: projectSchema,
        validateOnChange: false
    });
    useEffect(() => {
        if (projects.isSuccess && projectId) {
            const project = projects.data.filter((e) => e.id === projectId)[0];
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            const { id, total_transactions, org_id, ...rest } = project;
            setSlugGenerate(!project);
            const value = {
                ...rest,
                org_id: org_id || ''
            };
            formik.setValues((old) => ({ ...old, ...value }));
        }
    }, [projects.status]);
    if (projects.isError)
        return (
            <>
                {console.error(projects.error)}
                <div>Error {projects.error.code}</div>
            </>
        );
    if (projects.isLoading) return <div>Loading...</div>;
    if (projects.isSuccess) {
        const options = [
            {
                value: 'tag1'
            },
            {
                value: 'tag2'
            },
            {
                value: 'tag3'
            },
            {
                value: 'tag4'
            },
            {
                value: 'tag5'
            },
            {
                value: 'tag6'
            }
        ];
        return (
            <div className="flex flex-col gap-3">
                <Container header="Project details">
                    <Form
                        name="project_details"
                        id={formId}
                        layout="vertical"
                        onSubmitCapture={formik.handleSubmit}
                        initialValues={{ tags: formik.values.tags, name: 'asdasd' }}
                        onFinishFailed={() => console.log(formik.errors)}
                        autoComplete="on"
                        noValidate={true}
                    >
                        <Row gutter={12}>
                            <Col span={12}>
                                <Form.Item<typeof FormikValues>
                                    label="Name"
                                    rules={[{ required: true }]}
                                    help={formik.errors.name}
                                    validateStatus={formik.errors.name ? 'error' : ''}
                                >
                                    <Input
                                        name="name"
                                        value={formik.values.name}
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
                            </Col>
                            <Col span={12}>
                                <Form.Item<typeof FormikValues>
                                    label="slug"
                                    rules={[{ required: true }]}
                                    help={formik.errors.slug}
                                    validateStatus={formik.errors.slug ? 'error' : ''}
                                >
                                    <Input
                                        name="slug"
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
                            </Col>
                        </Row>
                        <Form.Item<typeof FormikValues>
                            label="Description"
                            help={formik.errors.description}
                            validateStatus={formik.errors.description ? 'error' : ''}
                        >
                            <Input.TextArea
                                name="description"
                                value={formik.values.description}
                                onChange={formik.handleChange}
                            />
                        </Form.Item>
                        <Form.Item<typeof FormikValues>
                            label="Tags"
                            validateStatus={formik.errors.tags ? 'error' : ''}
                            help={formik.errors.tags}
                        >
                            <Select
                                mode="tags"
                                allowClear
                                value={formik.values.tags}
                                tagRender={({ value, closable, onClose }) => {
                                    return (
                                        <Tag color="magenta" closable={closable} onClose={onClose}>
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
                                options={options}
                            />
                        </Form.Item>
                    </Form>
                </Container>
                <ProviderFormAndList
                    ProvidersList={formik.values.ai_providers}
                    setProvidersList={(list: typeof FormikValues.ai_providers) =>
                        formik.setValues({ ...formik.values, ai_providers: list })
                    }
                    projectSlug={formik.values.slug}
                    isProjects={!!projectId}
                    isError={!!formik.errors.ai_providers}
                />
            </div>
        );
    }
};

export default ProjectForm;
