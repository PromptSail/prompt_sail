import { Accordion, Button, Form, InputGroup } from 'react-bootstrap';
import { FormikValues } from './types';
import { SetStateAction, useEffect, useState } from 'react';
import { useFormik } from 'formik';
import { providerSchema } from '../../api/formSchemas';

interface Props {
    ProvidersList: typeof FormikValues.ai_providers;
    setProvidersList: (list: SetStateAction<typeof FormikValues.ai_providers>) => void;
    slug: string;
    toSlug: (text: string) => string;
    errorMessage: string;
}

const ProviderFormAndList: React.FC<Props> = ({
    ProvidersList,
    setProvidersList,
    slug,
    toSlug,
    errorMessage
}) => {
    const [FormShowed, setFormShow] = useState(ProvidersList.length < 1);
    const [EditedProvider, setEditedProvider] = useState<number | null>(null);
    const formik = useFormik({
        initialValues: {
            deployment_name: '',
            description: '',
            api_base: '',
            provider_name: ''
        },
        onSubmit: async ({ deployment_name, provider_name, api_base, description }) => {
            if (
                ProvidersList.filter((e) => toSlug(e.deployment_name) === toSlug(deployment_name))
                    .length > 0
            ) {
                formik.setErrors({ deployment_name: 'Name must be unique' });
            } else {
                formik.setErrors({});
                setProvidersList((old) => [
                    ...old,
                    { api_base, provider_name, deployment_name, description }
                ]);
                setFormShow(false);
            }
        },
        validateOnChange: false,
        validationSchema: providerSchema
    });
    const makeUrl = (slug: string, name: string) => {
        return `http://${toSlug(slug) || '<slug>'}/${toSlug(name) || '<name>'}`;
    };
    useEffect(() => {
        if (EditedProvider !== null) {
            formik.setValues((old) => ({ ...old, ...ProvidersList[EditedProvider] }));
        }
    }, [EditedProvider]);
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
                                <Button
                                    variant={`${EditedProvider != id ? 'outline-' : ''}secondary`}
                                    onClick={() => {
                                        if (EditedProvider != id) {
                                            setEditedProvider(id);
                                            setFormShow(true);
                                        } else {
                                            setEditedProvider(null);
                                            setFormShow(false);
                                        }
                                    }}
                                >
                                    {`${EditedProvider != id ? '' : 'Cancel '}edit`}
                                </Button>
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
                <div className={`ai-providers${formik.isValid ? '' : ' error'}`}>
                    <form
                        className="inputs"
                        id="providersForm"
                        onSubmit={formik.handleSubmit}
                        noValidate
                    >
                        <InputGroup>
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
                            <Form.Control.Feedback type="invalid" tooltip>
                                {formik.errors.provider_name}
                            </Form.Control.Feedback>
                        </InputGroup>
                        <InputGroup>
                            <InputGroup.Text>Deployment name</InputGroup.Text>
                            <Form.Control
                                type="text"
                                name={`deployment_name`}
                                onChange={formik.handleChange}
                                value={formik.values.deployment_name}
                                isInvalid={!!formik.errors.deployment_name}
                            />
                            <Form.Control.Feedback type="invalid" tooltip>
                                {formik.errors.deployment_name}
                            </Form.Control.Feedback>
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
                            <Form.Control.Feedback type="invalid" tooltip>
                                {formik.errors.api_base}
                            </Form.Control.Feedback>
                        </InputGroup>
                    </form>
                    <div className="calculated-link">
                        {makeUrl(slug, formik.values.deployment_name)}
                    </div>
                    {EditedProvider !== null && (
                        <Button
                            variant="dark"
                            onClick={() => {
                                const update = ProvidersList.map((el, id) => {
                                    if (id == EditedProvider) return formik.values;
                                    else return el;
                                });
                                setProvidersList(update);
                                setEditedProvider(null);
                                setFormShow(false);
                            }}
                        >
                            Update AI Provider
                        </Button>
                    )}
                    {EditedProvider === null && (
                        <Button type="submit" form="providersForm" variant="dark">
                            Add Ai Provider
                        </Button>
                    )}
                    {!!errorMessage && <p className="no-providers-error">{errorMessage}</p>}
                </div>
            )}
            {!FormShowed && (
                <Button
                    className="add-another-provider"
                    variant="dark"
                    onClick={() => {
                        setFormShow(true);
                        formik.setValues((old) => ({ ...old, deployment_name: '' }));
                    }}
                >
                    Add another AI Provider
                </Button>
            )}
        </>
    );
};
export default ProviderFormAndList;
