import { useFormik } from 'formik';
import { useEffect, useState } from 'react';
import { Form } from 'react-bootstrap';
import ProviderFormAndList from './ProviderFormAndList';
import { projectSchema } from '../../api/formSchemas';
import { useGetAllProjects } from '../../api/queries';
import { toSlug } from '../../helpers/aiProvider';
import Helper from './helper';

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
            <div className="forms">
                <div className="project-form">
                    <h2 className="header">Project details</h2>
                    <form className={`box`} id={formId} onSubmit={formik.handleSubmit} noValidate>
                        <div className="double-inputs">
                            <Form.Group className="labeled-input">
                                <Form.Label>Name</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="name"
                                    onChange={formik.handleChange}
                                    value={formik.values.name}
                                    onKeyUp={(e) => {
                                        const val = e.currentTarget.value;
                                        if (isSlugGenerated)
                                            formik.setValues((old) => ({
                                                ...old,
                                                slug: toSlug(val)
                                            }));
                                    }}
                                    isInvalid={!!formik.errors.name}
                                />
                                <Form.Control.Feedback type="invalid">
                                    {formik.errors.name}
                                </Form.Control.Feedback>
                            </Form.Group>
                            <Form.Group className="labeled-input">
                                <Form.Label>
                                    Slug
                                    <Helper>
                                        Slug is a unique name used to identify a project in the
                                        proxy URL
                                    </Helper>
                                </Form.Label>

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
                                    isInvalid={!!formik.errors.slug}
                                />
                                <Form.Control.Feedback type="invalid">
                                    {formik.errors.slug}
                                </Form.Control.Feedback>
                            </Form.Group>
                        </div>
                        <Form.Group className="labeled-input">
                            <Form.Label>Description</Form.Label>
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
                            <Form.Control.Feedback type="invalid">
                                {formik.errors.description}
                            </Form.Control.Feedback>
                        </Form.Group>
                        <Form.Group className="labeled-input">
                            <Form.Label>Tags</Form.Label>
                            <Form.Control
                                name="tags"
                                onChange={formik.handleChange}
                                value={formik.values.tags}
                                isInvalid={!!formik.errors.tags}
                            />
                            <Form.Control.Feedback type="invalid">
                                {formik.errors.tags}
                            </Form.Control.Feedback>
                        </Form.Group>
                    </form>
                </div>
                <ProviderFormAndList
                    ProvidersList={formik.values.ai_providers}
                    setProvidersList={(list: typeof FormikValues.ai_providers) =>
                        formik.setValues({ ...formik.values, ai_providers: list })
                    }
                    projectSlug={formik.values.slug}
                    isProjects={!!projectId}
                    errorMessage={formik.errors.ai_providers as string}
                />
            </div>
        );
};

export default ProjectForm;
