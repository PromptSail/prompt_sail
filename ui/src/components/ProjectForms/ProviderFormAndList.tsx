import { Accordion, Button, Form, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { FormikValues } from './types';
import { useState } from 'react';
import { useFormik } from 'formik';
import { providerSchema } from '../../api/formSchemas';
import { makeUrl, toSlug } from '../../helpers/aiProvider';
import Helper from './helper';
import { useGetProviders } from '../../api/queries';

interface Props {
    ProvidersList: typeof FormikValues.ai_providers;
    setProvidersList: (list: typeof FormikValues.ai_providers) => void;
    projectSlug: string;
    errorMessage: string;
    isProjects: boolean;
}

const ProviderFormAndList: React.FC<Props> = ({
    ProvidersList,
    setProvidersList,
    projectSlug,
    errorMessage,
    isProjects
}) => {
    const [EditedProvider, setEditedProvider] = useState<number | null>(null);
    const [FormShowed, setFormShow] = useState(!isProjects);
    const providers = useGetProviders();
    const ProviderForm: React.FC = () => {
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
            onSubmit: async ({ deployment_name, provider_name, api_base, description }) => {
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
            <form
                className={`box${errorMessage ? ' invalid' : ''}`}
                onSubmit={formik.handleSubmit}
                noValidate
            >
                <div className="double-inputs">
                    <Form.Group className="labeled-input">
                        <Form.Label>AI Providers</Form.Label>
                        <Form.Select
                            name={`provider_name`}
                            onChange={(e) => {
                                formik.handleChange(e);
                                const prov = providers.data?.data.filter(
                                    (el) => el.provider_name === e.target.value
                                )[0];
                                setApiBasePlaceholder(
                                    prov?.api_base_placeholder || 'http://your.url'
                                );
                            }}
                            value={formik.values.provider_name}
                            aria-placeholder="Select provider"
                            isInvalid={!!formik.errors.provider_name}
                        >
                            <option value="" key={null}>
                                Select provider
                            </option>
                            {providers.isLoading && (
                                <option value={'loading'} key={`loading`}>
                                    loading...
                                </option>
                            )}
                            {providers.isError && (
                                <option value={'error'} key={`error`}>
                                    {`${providers.error.code}:${providers.error.message}`}
                                </option>
                            )}
                            {providers.isSuccess &&
                                providers.data.data.map((el, id) => (
                                    <option
                                        onClick={() =>
                                            setApiBasePlaceholder(el.api_base_placeholder)
                                        }
                                        value={el.provider_name}
                                        key={`${el.provider_name}${id}`}
                                    >
                                        {el.provider_name}
                                    </option>
                                ))}
                        </Form.Select>
                        <Form.Control.Feedback type="invalid">
                            {formik.errors.provider_name}
                        </Form.Control.Feedback>
                    </Form.Group>
                    <Form.Group className="labeled-input">
                        <Form.Label>
                            Deployment name
                            <Helper>
                                Enter a unique name for your deployment from the AI provider to
                                identify it in the proxy URL
                            </Helper>
                        </Form.Label>
                        <Form.Control
                            type="text"
                            name={`deployment_name`}
                            onChange={formik.handleChange}
                            value={formik.values.deployment_name}
                            isInvalid={!!formik.errors.deployment_name}
                        />
                        <Form.Control.Feedback type="invalid">
                            {formik.errors.deployment_name}
                        </Form.Control.Feedback>
                    </Form.Group>
                </div>
                <Form.Group className="labeled-input">
                    <Form.Label>
                        Api base URL
                        <Helper>
                            Enter the base URL for the LLM endpoint you want to connect with
                        </Helper>
                    </Form.Label>
                    <Form.Control
                        type="url"
                        name={`api_base`}
                        onChange={formik.handleChange}
                        value={formik.values.api_base}
                        placeholder={apiBasePlaceholder}
                        isInvalid={!!formik.errors.api_base}
                    />
                    <Form.Control.Feedback type="invalid">
                        {formik.errors.api_base}
                    </Form.Control.Feedback>
                </Form.Group>
                <Form.Group className="labeled-input">
                    <Form.Label>
                        Proxy URL
                        <Helper>
                            A proxy URL is auto-generated from the project slug and the deployment
                            name and is used to capture and log all interactions with LLM provider
                        </Helper>
                    </Form.Label>
                    <Form.Control
                        type="text"
                        className="generated-link"
                        onChange={formik.handleChange}
                        value={makeUrl(projectSlug, formik.values.deployment_name)}
                        disabled
                    />
                    <Form.Control.Feedback type="invalid"></Form.Control.Feedback>
                </Form.Group>
                <Button type="submit" variant="secondary">
                    {EditedProvider != undefined ? 'Update AI Provider' : 'Add Ai Provider'}
                </Button>
            </form>
        );
    };
    return (
        <div className="providers-form">
            <div className="header">
                <h2>Provider details</h2>
                <p>
                    <span className={errorMessage ? 'no-providers-error' : ''}>
                        Add at least one AI provider
                    </span>
                    , to use PromptSail as a proxy server for collecting{' '}
                    <OverlayTrigger
                        placement="bottom"
                        overlay={
                            <Tooltip>
                                A transaction consists of a request sent to an LLM provider and a
                                response received to the request.
                            </Tooltip>
                        }
                    >
                        <span style={{ textDecoration: 'underline', fontWeight: 'bold' }}>
                            transactions
                        </span>
                    </OverlayTrigger>{' '}
                    in the project
                </p>
            </div>
            {ProvidersList.length > 0 && (
                <Accordion>
                    {ProvidersList.map((el, id) => (
                        <Accordion.Item eventKey={`${id}`} key={id} className="box">
                            <Accordion.Header>
                                <span>{el.deployment_name}</span>
                                <span>{makeUrl(projectSlug, el.deployment_name)}</span>
                            </Accordion.Header>
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
                                        variant="dark"
                                        onClick={() => {
                                            if (EditedProvider != id) {
                                                setEditedProvider(id);
                                                setFormShow(false);
                                            } else setEditedProvider(null);
                                        }}
                                    >
                                        {`${EditedProvider != id ? '' : 'Cancel '}Edit`}
                                    </Button>
                                    <Button
                                        variant="danger"
                                        onClick={() => {
                                            const newList = ProvidersList.filter(
                                                (_el, idx) => idx != id
                                            );
                                            setProvidersList(newList);
                                            if (newList.length < 1) setFormShow(true);
                                        }}
                                    >
                                        Delete
                                    </Button>
                                </div>
                                {EditedProvider == id && <ProviderForm />}
                            </Accordion.Body>
                        </Accordion.Item>
                    ))}
                </Accordion>
            )}
            {FormShowed && <ProviderForm />}
            {!FormShowed && !EditedProvider && (
                <Button
                    variant="dark"
                    className="add-another-provider"
                    onClick={() => {
                        setFormShow(true);
                        setEditedProvider(null);
                    }}
                >
                    Add another AI Provider
                </Button>
            )}
        </div>
    );
};
export default ProviderFormAndList;
