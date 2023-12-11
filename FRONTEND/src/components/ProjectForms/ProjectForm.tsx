import { FormikHandlers, FormikValues } from 'formik';
import { Button, Form, InputGroup, Modal } from 'react-bootstrap';

interface Props {
    handleChange: FormikHandlers['handleChange'];
    handleSubmit: FormikHandlers['handleSubmit'];
    values: FormikValues;
    showHandler: {
        isShow: boolean;
        setShow: React.Dispatch<React.SetStateAction<boolean>>;
    };
}

const ProjectForm: React.FC<Props> = ({ handleChange, handleSubmit, values, showHandler }) => {
    const { isShow, setShow } = showHandler;
    return (
        <Modal show={isShow} onHide={() => setShow((e) => !e)}>
            <form onSubmit={handleSubmit} noValidate>
                <Modal.Header closeButton>
                    <Modal.Title>Edit Project</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Name</InputGroup.Text>
                        <Form.Control
                            type="text"
                            name="name"
                            onChange={handleChange}
                            value={values.name}
                            required
                        />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Slug</InputGroup.Text>
                        <Form.Control
                            type="text"
                            name="slug"
                            onChange={handleChange}
                            value={values.slug}
                            required
                        />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Description</InputGroup.Text>
                        <Form.Control
                            as="textarea"
                            name="description"
                            onChange={handleChange}
                            value={values.description}
                            rows={4}
                            cols={50}
                            maxLength={280}
                            required
                        />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>API Base URL</InputGroup.Text>
                        <Form.Control
                            type="url"
                            name="api_base"
                            onChange={handleChange}
                            value={values.api_base}
                            placeholder="https://api.openai.com/v1"
                            required
                        />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Provider name</InputGroup.Text>
                        <Form.Select
                            name="provider_name"
                            onChange={handleChange}
                            value={values.provider_name}
                        >
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
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Model name</InputGroup.Text>
                        <Form.Control
                            type="text"
                            name="ai_model_name"
                            onChange={handleChange}
                            value={values.ai_model_name}
                            required
                        />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Tags</InputGroup.Text>
                        <Form.Control
                            as="textarea"
                            name="tags"
                            onChange={handleChange}
                            value={values.tags}
                            rows={4}
                            cols={50}
                            required
                        />
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Text>Organization</InputGroup.Text>
                        <Form.Control
                            type="text"
                            name="org_id"
                            onChange={handleChange}
                            value={values.org_id}
                        />
                    </InputGroup>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShow((e) => !e)}>
                        Close
                    </Button>
                    <Button variant="primary" type="submit">
                        Save Changes
                    </Button>
                </Modal.Footer>
            </form>
        </Modal>
    );
};

export default ProjectForm;
