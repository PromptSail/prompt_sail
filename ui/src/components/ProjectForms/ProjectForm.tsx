import { useFormik } from 'formik';
import { ReactNode, useEffect, useState } from 'react';
import { Form, InputGroup, OverlayTrigger, Tooltip } from 'react-bootstrap';
import slugify from 'slugify';
import ProviderFormAndList from './ProviderFormAndList';
import { projectSchema } from '../../api/formSchemas';
import { useGetAllProjects } from '../../api/queries';

const FormikValues = {
    name: '',
    slug: '',
    description: '',
    ai_providers: [
        {
            deployment_name: '',
            slug: '',
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
    formId: string;
    projectId?: string;
}

const ProjectForm: React.FC<Props> = ({ submitFunc, formId, projectId }) => {
    const projects = useGetAllProjects();
    const [isSlugGenerated, setSlugGenerate] = useState(true);
    const formik = useFormik({
        initialValues: { ...FormikValues, ai_providers: [] as typeof FormikValues.ai_providers },
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
    const Info: React.FC<{ children: ReactNode }> = ({ children }) => {
        return (
            <OverlayTrigger placement="right" overlay={<Tooltip>{children}</Tooltip>}>
                <span
                    style={{
                        position: 'absolute',
                        right: '-30px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        border: '2px solid #555555',
                        borderRadius: '50%',
                        aspectRatio: '1/1',
                        padding: '.5em',
                        lineHeight: '5px',
                        margin: 'auto',
                        fontFamily: 'serif',
                        fontWeight: 'bold'
                    }}
                >
                    i
                </span>
            </OverlayTrigger>
        );
    };
    useEffect(() => {
        if (projects.isSuccess && projectId) {
            const project = projects.data.filter((e) => e.id === projectId)[0];
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            const { id, total_transactions, tags, org_id, ...rest } = project;
            setSlugGenerate(!project);
            const value = {
                ...rest,
                tags: tags.join(', '),
                org_id: org_id || ''
            };
            formik.setValues((old) => ({ ...old, ...value }));
        }
    }, [projects.status]);
    const toSlug = (text: string) => {
        const newText = text.replace(/^\d+|[@*()+:'"~]/g, '');
        return slugify(newText, {
            replacement: '-',
            lower: true
        });
    };
    if (projects.isError)
        return (
            <>
                {console.error(projects.error)}
                <div>Error {projects.error.code}</div>
            </>
        );
    if (projects.isLoading) return <div>Loading...</div>;
    if (projects.isSuccess)
        return (
            <div>
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
                        <Info>
                            Slug is a URL-friendly name used to identify a project. It's utilized in
                            the URL for adding transactions
                        </Info>
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
                    ProvidersList={formik.values.ai_providers}
                    setProvidersList={(list: typeof FormikValues.ai_providers) =>
                        formik.setValues({ ...formik.values, ai_providers: list })
                    }
                    projectSlug={formik.values.slug}
                    toSlug={toSlug}
                    isProjects={!!projectId}
                    errorMessage={formik.errors.ai_providers as string}
                />
            </div>
        );
};

export default ProjectForm;
