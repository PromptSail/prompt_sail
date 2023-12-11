import api from '../api/api';
import { useState } from 'react';
import ProjetTile from '../components/projectTile/projectTile';
import { addProjectRequest, getAllProjects } from '../api/interfaces';
import { Link } from 'react-router-dom';
import { Button, Form, InputGroup, Modal } from 'react-bootstrap';
import { useFormik } from 'formik';
import { useGetAllProjects } from '../api/queries';
import { toast } from 'react-toastify';
import { addProjectSchema } from '../api/formSchemas';

const Dashboard = () => {
    const projects = useGetAllProjects();
    const [filter, setFilter] = useState('');
    const [showModal, setShowModal] = useState(false);
    const filterProjects = (data: getAllProjects) => {
        return (
            data.name.includes(filter) ||
            data.slug.includes(filter) ||
            data.description.includes(filter) ||
            data.tags.join(', ').includes(filter)
        );
    };
    const formik = useFormik({
        initialValues: {
            name: '',
            slug: '',
            description: '',
            api_base: '',
            provider_name: '',
            ai_model_name: '',
            tags: '',
            org_id: ''
        },
        onSubmit: async ({
            name,
            slug,
            description,
            api_base,
            provider_name,
            ai_model_name,
            tags,
            org_id
        }) => {
            const reqValues: addProjectRequest = {
                name,
                slug,
                description,
                ai_providers: [
                    {
                        api_base,
                        provider_name,
                        ai_model_name
                    }
                ],
                tags: tags.replace(/\s/g, '').split(','),
                org_id
            };
            console.log(reqValues);
            await api
                .addProject(reqValues)
                .then(() => {
                    setShowModal((e) => !e);
                    toast.success('Project successfully added', {
                        position: 'bottom-left',
                        autoClose: 1000,
                        theme: 'colored'
                    });
                    projects.refetch();
                })
                .catch((err) => console.error(err));
        },
        validateOnChange: true,
        validationSchema: addProjectSchema
    });
    if (projects.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (projects.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.log(projects.error)}
            </>
        );
    if (projects.isSuccess) {
        // filterPorjects(() => projects.data);
        return (
            <>
                <div className="w-5/6 m-auto">
                    <div className="flex flex-row justify-between">
                        <div className="flex flex-col">
                            <h2 className="text-3xl font-semibold text-left">Projects</h2>
                            <div className="flex flex-row">
                                <span>17 members</span>
                                <span>30 projects</span>
                            </div>
                        </div>
                        <div className="flex flex-row gap-2">
                            <Form.Control
                                className="m-auto"
                                type="text"
                                name="search"
                                placeholder="Search"
                                onChange={(e) => {
                                    const val = e.currentTarget.value;
                                    if (val.length > 2) setFilter(val);
                                    else if (filter != '') setFilter('');
                                }}
                            />
                            <Button
                                variant="primary"
                                className="m-auto whitespace-nowrap"
                                onClick={() => setShowModal((e) => !e)}
                            >
                                New Project +
                            </Button>
                        </div>
                    </div>
                    <div className="grid grid-cols-1 py-5 gap-3 md:grid-cols-2">
                        {projects.data
                            .filter((el) => filterProjects(el))
                            .map((project: getAllProjects, id: number) => (
                                <Link to={`/projects/${project.id}`} key={project.id}>
                                    <ProjetTile key={id} data={project} />
                                </Link>
                            ))}
                    </div>
                    <div></div>
                </div>
                <Modal show={showModal} onHide={() => setShowModal((e) => !e)}>
                    <form onSubmit={formik.handleSubmit} noValidate>
                        <Modal.Header closeButton>
                            <Modal.Title>Add project</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            <InputGroup className="mb-3">
                                <InputGroup.Text>Name</InputGroup.Text>
                                <Form.Control
                                    type="text"
                                    name="name"
                                    onChange={formik.handleChange}
                                    required
                                />
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <InputGroup.Text>Slug</InputGroup.Text>
                                <Form.Control
                                    type="text"
                                    name="slug"
                                    onChange={formik.handleChange}
                                    required
                                />
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <InputGroup.Text>Description</InputGroup.Text>
                                <Form.Control
                                    as="textarea"
                                    name="description"
                                    onChange={formik.handleChange}
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
                                    onChange={formik.handleChange}
                                    placeholder="https://api.openai.com/v1"
                                    required
                                />
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <InputGroup.Text>Provider name</InputGroup.Text>
                                <Form.Select name="provider_name" onChange={formik.handleChange}>
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
                                    onChange={formik.handleChange}
                                    required
                                />
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <InputGroup.Text>Tags</InputGroup.Text>
                                <Form.Control
                                    as="textarea"
                                    name="tags"
                                    onChange={formik.handleChange}
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
                                    onChange={formik.handleChange}
                                />
                            </InputGroup>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={() => setShowModal((e) => !e)}>
                                Close
                            </Button>
                            <Button variant="primary" type="submit">
                                Save Changes
                            </Button>
                        </Modal.Footer>
                    </form>
                </Modal>
            </>
        );
    }
};

export default Dashboard;
