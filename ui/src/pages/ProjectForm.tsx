import { useFormik } from 'formik';
import { useEffect, useRef, useState } from 'react';
import { Button, Form, InputGroup } from 'react-bootstrap';
import slugify from 'slugify';
import * as yup from 'yup';
import ProviderFormAndList from '../components/ProjectForms/ProviderFormAndList';
import { getProjectResponse } from '../api/interfaces';

const FormikValues = {
    name: '',
    slug: '',
    description: '',
    ai_providers: [
        {
            deployment_name: '',
            api_base: '',
            description: '',
            provider_name: ''
        }
    ],
    tags: '',
    org_id: ''
};
interface Props {
    submitFunc: (values: typeof FormikValues) => Promise<void>;
    validationSchema: yup.AnyObjectSchema;
    formId: string;
    project?: getProjectResponse;
}

const ProjectForm: React.FC<Props> = ({ submitFunc, validationSchema, formId, project }) => {
    const [aiProviders, setAiProviders] = useState<typeof FormikValues.ai_providers>(
        project ? project.ai_providers : []
    );
    const [isSlugGenerated, setSlugGenerate] = useState(!project);
    const providerErrorRef = useRef(null);
    const formik = useFormik({
        initialValues: FormikValues,
        onSubmit: async (values) => {
            console.log(values);
            if (aiProviders.length > 0)
                submitFunc({
                    ...values,
                    slug: toSlug(values.slug),
                    ai_providers: aiProviders
                });
            else {
                if (providerErrorRef.current) {
                    const error = providerErrorRef.current as HTMLParagraphElement;
                    console.log(error);
                    error.style.display = 'block';
                }
            }
        },
        validationSchema,
        validateOnChange: false
    });
    useEffect(() => {
        if (project) {
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            const { id, total_transactions, ai_providers, ...rest } = project;
            const value = {
                ...rest,
                tags: project.tags.join(', '),
                org_id: project.org_id || ''
            };
            formik.setValues((old) => ({ ...old, ...value }));
        }
    }, [project]);
    const toSlug = (text: string) => {
        return slugify(text, { replacement: '-', lower: true });
    };
    return (
        <div>
            <Button onClick={() => console.log(formik.errors)}></Button>
            <form id={formId} onSubmit={formik.handleSubmit} noValidate>
                <InputGroup className="mb-3">
                    <InputGroup.Text>Name</InputGroup.Text>
                    <Form.Control
                        type="text"
                        name="name"
                        onChange={formik.handleChange}
                        value={formik.values.name}
                        onKeyUp={(e) => {
                            const val = e.currentTarget.value;
                            if (isSlugGenerated)
                                formik.setValues((old) => ({ ...old, slug: toSlug(val) }));
                        }}
                        required
                        isInvalid={!!formik.errors.name}
                    />
                    <Form.Control.Feedback type="invalid" tooltip>
                        {formik.errors.name}
                    </Form.Control.Feedback>
                </InputGroup>
                <InputGroup className="mb-3">
                    <InputGroup.Text>Slug</InputGroup.Text>
                    <Form.Control
                        type="text"
                        name="slug"
                        onKeyDown={() => setSlugGenerate(false)}
                        onBlur={(e) => {
                            const val = e.currentTarget.value;
                            if (val.length < 1) setSlugGenerate(true);
                            e.currentTarget.value = toSlug(val);
                        }}
                        onChange={formik.handleChange}
                        value={formik.values.slug}
                        required
                        isInvalid={!!formik.errors.slug}
                    />
                    <Form.Control.Feedback type="invalid" tooltip>
                        {formik.errors.slug}
                    </Form.Control.Feedback>
                </InputGroup>
                <InputGroup className="mb-3">
                    <InputGroup.Text>Description</InputGroup.Text>
                    <Form.Control
                        as="textarea"
                        name="description"
                        onChange={formik.handleChange}
                        value={formik.values.description}
                        rows={4}
                        cols={50}
                        maxLength={280}
                        isInvalid={!!formik.errors.description}
                    />
                    <Form.Control.Feedback type="invalid" tooltip>
                        {formik.errors.description}
                    </Form.Control.Feedback>
                </InputGroup>
                <InputGroup className="mb-3">
                    <InputGroup.Text>Tags</InputGroup.Text>
                    <Form.Control
                        as="textarea"
                        name="tags"
                        onChange={formik.handleChange}
                        value={formik.values.tags}
                        rows={4}
                        cols={50}
                        isInvalid={!!formik.errors.tags}
                    />
                    <Form.Control.Feedback type="invalid" tooltip>
                        {formik.errors.tags}
                    </Form.Control.Feedback>
                </InputGroup>
            </form>
            <ProviderFormAndList
                providerErrorRef={providerErrorRef}
                ProvidersList={aiProviders}
                setProvidersList={setAiProviders}
                slug={formik.values.slug}
                toSlug={toSlug}
            />
        </div>
    );
};

export default ProjectForm;
