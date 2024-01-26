import { useFormik } from 'formik';
import { useState } from 'react';
import { Accordion, Button, Form, InputGroup } from 'react-bootstrap';
import slugify from 'slugify';
import * as yup from 'yup';

const FormikValues = {
    name: '',
    slug: '',
    description: '',
    ai_providers: [
        {
            api_base: '',
            provider_name: '',
            ai_model_name: ''
        }
    ],
    tags: '',
    org_id: ''
};
interface Props {
    onSubmit: (values: typeof FormikValues) => Promise<void>;
    validationSchema: yup.AnyObjectSchema;
}

const ProjectForm: React.FC<Props> = ({ onSubmit, validationSchema }) => {
    const [aiProviders, setAiProviders] = useState<typeof FormikValues.ai_providers>([]);
    const [ProviderIndex, setProviderIndex] = useState(0);
    const [isProviderFormShowed, setProviderForm] = useState(true);
    const [isSlugGenerated, setSlugGenerate] = useState(true);
    const formik = useFormik({
        initialValues: FormikValues,
        onSubmit: onSubmit,
        validationSchema,
        validateOnChange: false
    });
    const toSlug = (text: string) => {
        return slugify(text, { replacement: '_', lower: true });
    };
    const addProvider = () => {
        formik.setStatus({ _form: '' });
        const id = ProviderIndex;
        const ai_model_name = formik.values.ai_providers[id].ai_model_name;
        const provider_name = formik.values.ai_providers[id].provider_name;
        const api_base = formik.values.ai_providers[id].api_base;
        if (!!ai_model_name && !!provider_name && !!api_base) {
            formik.setErrors({
                ...formik.errors,
                ai_providers: undefined
            });
            setAiProviders((old) => [...old, { api_base, provider_name, ai_model_name }]);
            formik.values.ai_providers.push(FormikValues.ai_providers[0]);
            setProviderIndex(formik.values.ai_providers.length - 1);
            setProviderForm(false);
        } else {
            formik.setErrors({
                ...formik.errors,
                ai_providers: [
                    {
                        api_base: api_base ? undefined : 'Required',
                        provider_name: provider_name ? undefined : 'Required',
                        ai_model_name: ai_model_name ? undefined : 'Required'
                    }
                ]
            });
        }
    };
    return (
        <form>
            <InputGroup className="mb-3">
                <InputGroup.Text>Name</InputGroup.Text>
                <Form.Control
                    type="text"
                    name="name"
                    onChange={formik.handleChange}
                    value={formik.values.name}
                    required
                    isInvalid={!!formik.errors.name}
                />
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
                    value={(() => {
                        if (isSlugGenerated) return toSlug(formik.values.name);
                        else formik.values.slug;
                    })()}
                    required
                    isInvalid={!!formik.errors.slug}
                />
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
                />
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
                />
            </InputGroup>
            <Accordion>
                {aiProviders.map((el, id) => (
                    <Accordion.Item eventKey={`${id}`} key={id}>
                        <Accordion.Header>{el.ai_model_name}</Accordion.Header>
                        <Accordion.Body>
                            <div className="content">
                                <span className="title">Provider:</span>
                                <span>{el.provider_name}</span>
                            </div>
                            <div className="content">
                                <span className="title">Api url:</span>
                                <span>{el.api_base}</span>
                            </div>
                            <div className="options">
                                <Button variant="outline-secondary">Edit</Button>
                                <Button
                                    onClick={() => {
                                        const newList = aiProviders.filter((el, idx) => idx != id);
                                        setAiProviders(newList);
                                        formik.values.ai_providers = [
                                            ...newList,
                                            FormikValues.ai_providers[0]
                                        ];
                                        if (ProviderIndex >= id)
                                            setProviderIndex(formik.values.ai_providers.length - 1);
                                    }}
                                    variant="outline-danger"
                                >
                                    Delete
                                </Button>
                            </div>
                        </Accordion.Body>
                    </Accordion.Item>
                ))}
            </Accordion>
            {(() => {
                const errors = formik.errors.ai_providers as typeof FormikValues.ai_providers;
                if (isProviderFormShowed)
                    return (
                        <div className={`ai-providers${errors ? ' error' : ''}`}>
                            <div className="inputs">
                                <Form.Select
                                    name={`ai_providers[${ProviderIndex}].provider_name`}
                                    onChange={formik.handleChange}
                                    value={formik.values.ai_providers[ProviderIndex].provider_name}
                                    aria-placeholder="Select provider"
                                    isInvalid={!!errors && !!errors[0].provider_name}
                                >
                                    <option value="" key={null}>
                                        Select provider
                                    </option>
                                    {[
                                        'OpenAI',
                                        'Azure OpenAI',
                                        'Google Palm',
                                        'Anthropic Cloud',
                                        'Meta LLama',
                                        'HuggingFace',
                                        'Custom'
                                    ].map((el, id) => (
                                        <option value={el} key={`${el}${id}`}>
                                            {el}
                                        </option>
                                    ))}
                                </Form.Select>
                                <InputGroup>
                                    <InputGroup.Text>Deployment name</InputGroup.Text>
                                    <Form.Control
                                        type="text"
                                        name={`ai_providers[${ProviderIndex}].ai_model_name`}
                                        onChange={formik.handleChange}
                                        value={
                                            formik.values.ai_providers[ProviderIndex].ai_model_name
                                        }
                                        isInvalid={!!errors && !!errors[0].ai_model_name}
                                    />
                                </InputGroup>
                                <InputGroup>
                                    <InputGroup.Text>API Base URL</InputGroup.Text>
                                    <Form.Control
                                        type="url"
                                        name={`ai_providers[${ProviderIndex}].api_base`}
                                        onChange={formik.handleChange}
                                        value={formik.values.ai_providers[ProviderIndex].api_base}
                                        placeholder="https://api.openai.com/v1"
                                        isInvalid={!!errors && !!errors[0].api_base}
                                    />
                                </InputGroup>
                            </div>
                            <div className="calculated-link">&nbsp;</div>
                            <Button onClick={addProvider}>Add Ai Provider</Button>
                            <Button
                                onClick={() => {
                                    console.log(formik.values);
                                }}
                            >
                                values
                            </Button>
                        </div>
                    );
            })()}
            {!isProviderFormShowed && (
                <Button onClick={() => setProviderForm((e) => !e)}>Add another AI Provider</Button>
            )}
        </form>
    );
};

export default ProjectForm;
