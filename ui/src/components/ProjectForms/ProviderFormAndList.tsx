import { Accordion, Button, Form, InputGroup } from 'react-bootstrap';
import { FormikValues } from './types';
import { MutableRefObject, SetStateAction, useState } from 'react';
import { useFormik } from 'formik';

interface Props {
    ProvidersList: typeof FormikValues.ai_providers;
    setProvidersList: (list: SetStateAction<typeof FormikValues.ai_providers>) => void;
    slug: string;
    toSlug: (text: string) => string;
    providerErrorRef: MutableRefObject<null>;
}

const ProviderFormAndList: React.FC<Props> = ({
    ProvidersList,
    setProvidersList,
    slug,
    toSlug,
    providerErrorRef
}) => {
    const [FormShowed, setFormShow] = useState(true);
    const formik = useFormik({
        initialValues: {
            deployment_name: '',
            description: '',
            api_base: '',
            provider_name: ''
        },
        onSubmit: async ({ deployment_name, provider_name, api_base, description }) => {
            if (!!deployment_name && !!provider_name && !!api_base) {
                setProvidersList((old) => [
                    ...old,
                    { api_base, provider_name, deployment_name, description }
                ]);
                setFormShow(false);
                formik.setStatus('');
            } else {
                formik.setStatus('error');
                formik.setErrors({
                    api_base: api_base ? undefined : 'Required',
                    provider_name: provider_name ? undefined : 'Required',
                    deployment_name: deployment_name ? undefined : 'Required'
                });
            }
        }
    });
    const makeUrl = (slug: string, name: string) => {
        return `http://${slug || '<slug>'}/${toSlug(name) || '<name>'}`;
    };
    return (
        <>
            <Accordion>
                {ProvidersList.map((el, id) => (
                    <Accordion.Item eventKey={`${id}`} key={id}>
                        <Accordion.Header>{el.deployment_name}</Accordion.Header>
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
                                        const newList = ProvidersList.filter(
                                            (_el, idx) => idx != id
                                        );
                                        setProvidersList(newList);
                                        if (newList.length < 1) setFormShow(true);
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
            {FormShowed && (
                <div className={`ai-providers ${formik.status}`}>
                    <form
                        className="inputs"
                        id="providersForm"
                        onSubmit={formik.handleSubmit}
                        noValidate
                    >
                        <Form.Select
                            name={`provider_name`}
                            onChange={formik.handleChange}
                            value={formik.values.provider_name}
                            aria-placeholder="Select provider"
                            isInvalid={!!formik.errors.provider_name}
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
                                name={`deployment_name`}
                                onChange={formik.handleChange}
                                value={formik.values.deployment_name}
                                isInvalid={!!formik.errors.deployment_name}
                            />
                        </InputGroup>
                        <InputGroup>
                            <InputGroup.Text>API Base URL</InputGroup.Text>
                            <Form.Control
                                type="url"
                                name={`api_base`}
                                onChange={formik.handleChange}
                                value={formik.values.api_base}
                                placeholder="https://api.openai.com/v1"
                                isInvalid={!!formik.errors.api_base}
                            />
                        </InputGroup>
                    </form>
                    <div className="calculated-link">
                        {makeUrl(slug, formik.values.deployment_name)}
                    </div>
                    <Button type="submit" form="providersForm">
                        Add Ai Provider
                    </Button>
                    <p className="no-providers-error" ref={providerErrorRef}>
                        You need to add at least one AI Provider
                    </p>
                </div>
            )}
            {!FormShowed && (
                <Button
                    onClick={() => {
                        setFormShow(true);
                    }}
                >
                    Add another AI Provider
                </Button>
            )}
        </>
    );
};
export default ProviderFormAndList;
