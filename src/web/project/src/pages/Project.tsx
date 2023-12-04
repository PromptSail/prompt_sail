import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import SyntaxHighlighter from 'react-syntax-highlighter';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { Button, InputGroup, Modal, Form } from 'react-bootstrap';
import { useDeleteProject, useGetProject, useUpdateProject } from '../api/Queries';
import { getProjectResponse, updateProjectRequest } from '../api/interfaces';
import { useFormik } from 'formik';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
const Project: React.FC = () => {
    const navigate = useNavigate();
    const { state } = useLocation();
    const params = useParams();
    const [isUpdateModalShowed, setUpdateModal] = useState(false);
    const [isDelModalShowed, setDeleteModal] = useState(false);
    const project: UseQueryResult<AxiosResponse<getProjectResponse>> = useGetProject(
        params.projectId || ''
    );
    const deleteProject = useDeleteProject();
    const updateProject = useUpdateProject();
    // const passTransactionData (link: string, data: Transaction) => {
    //     history.pushState
    // }
    const formik = useFormik({
        enableReinitialize: true,
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
            const reqValues: updateProjectRequest = {
                id: params.projectId || '',
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
            updateProject.mutateAsync(reqValues).then(() => {
                setUpdateModal((e) => !e);
                project.refetch();
            });
        }
    });
    useEffect(() => {
        if (project.isSuccess) {
            const data = project.data.data;
            if (state !== null) {
                const transactionData = data.transactions.filter((el) => el.id == state);
                if (transactionData.length > 0) {
                    console.log(params.projectId);
                    console.log(state);
                    navigate(`/projects/${params.projectId}/transaction/${state}`, {
                        state: {
                            transaction: transactionData[0],
                            project: {
                                id: data.id,
                                name: data.name,
                                api_base: data.ai_providers[0].api_base
                            }
                        }
                    });
                } else {
                    console.log(2);
                    navigate('/');
                }
            }
            formik.setValues({
                name: data.name,
                slug: data.slug,
                description: data.description,
                api_base: data.ai_providers[0].api_base,
                provider_name: data.ai_providers[0].provider_name,
                ai_model_name: data.ai_providers[0].ai_model_name,
                tags: data.tags.join(', '),
                org_id: data.org_id
            });
        }
    }, [project.isSuccess]);
    if (project.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (project.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(project.error)}
                {navigate('/')}
            </>
        );
    if (project.isSuccess) {
        const data = project.data.data;
        return (
            <>
                <div className="m-auto mb-5 mt-[100px] max-w-[80%]">
                    <Button
                        variant="primary"
                        className="m-auto"
                        onClick={() => setDeleteModal((e) => !e)}
                    >
                        Delete
                    </Button>
                    <div>
                        <Button variant="primary" onClick={() => setUpdateModal((e) => !e)}>
                            Edit
                        </Button>
                        <Modal show={isUpdateModalShowed} onHide={() => setUpdateModal((e) => !e)}>
                            <form onSubmit={formik.handleSubmit}>
                                <Modal.Header closeButton>
                                    <Modal.Title>Edit Project</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <InputGroup className="mb-3">
                                        <InputGroup.Text>Name</InputGroup.Text>
                                        <Form.Control
                                            type="text"
                                            name="name"
                                            onChange={formik.handleChange}
                                            value={formik.values['name']}
                                            required
                                        />
                                    </InputGroup>
                                    <InputGroup className="mb-3">
                                        <InputGroup.Text>Slug</InputGroup.Text>
                                        <Form.Control
                                            type="text"
                                            name="slug"
                                            onChange={formik.handleChange}
                                            value={formik.values['slug']}
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
                                            value={formik.values['description']}
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
                                            value={formik.values['api_base']}
                                            placeholder="https://api.openai.com/v1"
                                            required
                                        />
                                    </InputGroup>
                                    <InputGroup className="mb-3">
                                        <InputGroup.Text>Provider name</InputGroup.Text>
                                        <Form.Select
                                            name="provider_name"
                                            onChange={formik.handleChange}
                                            value={formik.values['provider_name']}
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
                                            onChange={formik.handleChange}
                                            value={formik.values['ai_model_name']}
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
                                            value={formik.values['tags']}
                                            required
                                        />
                                    </InputGroup>
                                    <InputGroup className="mb-3">
                                        <InputGroup.Text>Organization</InputGroup.Text>
                                        <Form.Control
                                            type="text"
                                            name="org_id"
                                            onChange={formik.handleChange}
                                            value={formik.values['org_id']}
                                            required
                                        />
                                    </InputGroup>
                                </Modal.Body>
                                <Modal.Footer>
                                    <Button
                                        variant="secondary"
                                        onClick={() => setUpdateModal((e) => !e)}
                                    >
                                        Close
                                    </Button>
                                    <Button variant="primary" type="submit">
                                        Save Changes
                                    </Button>
                                </Modal.Footer>
                            </form>
                        </Modal>
                        <Modal show={isDelModalShowed} onHide={() => setDeleteModal((e) => !e)}>
                            <Modal.Header closeButton>
                                <Modal.Title>Delete {data.name}</Modal.Title>
                            </Modal.Header>

                            <Modal.Body>
                                <p>Are you sure you want to delete this project?</p>
                            </Modal.Body>

                            <Modal.Footer>
                                <Button
                                    variant="secondary"
                                    onClick={() => setDeleteModal((e) => !e)}
                                >
                                    No
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        deleteProject.mutateAsync(params.projectId || '');
                                    }}
                                >
                                    Yes
                                </Button>
                            </Modal.Footer>
                        </Modal>
                        <div
                            className="modal fade"
                            id="updateProjectModal"
                            tabIndex={-1}
                            aria-labelledby="updateProjectModalLabel"
                            aria-hidden="true"
                        ></div>
                    </div>
                    <h1 className="text-3xl font-semibold text-center mb-5 md:text-5xl">
                        {data.name}
                    </h1>
                    <h2 className="text-2xl font-semibold mb-2 md:text-4xl">Project details:</h2>
                    <p className="mb-5">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rutrum
                        dapibus lorem quis hendrerit. Fusce eu sapien at lacus facilisis tincidunt
                        eu ut quam. Ut quis lectus quis tortor vehicula fermentum vitae id nibh.
                        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
                        inceptos himenaeos. Sed vel tortor eget eros pulvinar blandit.
                    </p>
                    <SyntaxHighlighter
                        language="python"
                        style={styles.atomOneDark}
                        customStyle={{ display: 'inline' }}
                    >{`http://${data.slug}.promptsail.local`}</SyntaxHighlighter>
                    <span className="hidden md:inline">&rArr;</span>
                    <span className="block md:hidden my-5 ms-3">&dArr;</span>
                    <SyntaxHighlighter
                        language="python"
                        style={styles.atomOneDark}
                        customStyle={{ display: 'inline' }}
                    >
                        {data.ai_providers[0].api_base}
                    </SyntaxHighlighter>
                    <h2 className="text-2xl font-semibold mb-2 md:text-4xl">Usage example</h2>
                    <p className="mb-5">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rutrum
                        dapibus lorem quis hendrerit. Fusce eu sapien at lacus facilisis tincidunt
                        eu ut quam. Ut quis lectus quis tortor vehicula fermentum vitae id nibh.
                        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
                        inceptos himenaeos. Sed vel tortor eget eros pulvinar blandit.
                    </p>
                    <h4 className="text-xl font-semibold mb-2 md:text-2xl">Using openai library</h4>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {`import openai openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = "http://${data.slug}.promptsail.local"
openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": "Generate poem made of 2 sentences."}], )`}
                    </SyntaxHighlighter>
                    <h4 className="text-xl font-semibold mb-2 mt-3 md:text-2xl">
                        Using langchain library
                    </h4>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {`from langchain.llms import OpenAI
llm = OpenAI(
    model_name="text-davinci-003",
    openai_api_base="http://${data.slug}.promptsail.local",
)
llm("Explaining the meaning of life in one sentence")`}
                    </SyntaxHighlighter>
                    <h4 className="text-xl font-semibold mb-2 mt-3 md:text-2xl">
                        LLM Transactions
                    </h4>
                    <div className="overflow-x-auto p-3">
                        <table className="table-auto rounded-md shadow-lg w-full">
                            <thead className="rounded-md bg-[#EEE] text-[#565656]">
                                <tr className="rounded-md">
                                    <th>Timestamp</th>
                                    <th>Request url</th>
                                    <th>Prompt</th>
                                    <th>Response</th>
                                    <th>Model</th>
                                    <th>Content Type</th>
                                    <th>Response status</th>
                                    <th>Usage</th>
                                    <th>More</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.transactions.length > 0 &&
                                    data.transactions.map((tr, id) => {
                                        return (
                                            <tr key={id}>
                                                <td>{tr.timestamp}</td>
                                                <td>{tr.request.url}</td>
                                                <td>
                                                    {(() => {
                                                        if (tr.request.content.messages) {
                                                            return tr.request.content.messages.map(
                                                                (m, id) => (
                                                                    <p
                                                                        title={m.role}
                                                                        key={`${m.role}${id}`}
                                                                    >
                                                                        {m.content}
                                                                    </p>
                                                                )
                                                            );
                                                        } else
                                                            return tr.request.content.prompt.map(
                                                                (p, id) => (
                                                                    <p
                                                                        title={`prompt_${id}`}
                                                                        key={`prompt_${id}`}
                                                                    >
                                                                        {p}
                                                                    </p>
                                                                )
                                                            );
                                                    })()}
                                                </td>
                                                <td>
                                                    {tr.response.content.choices.map((c, id) => {
                                                        if (c.message) {
                                                            return (
                                                                <p
                                                                    title={c.message.role}
                                                                    key={`${c.message.role}${id}`}
                                                                >
                                                                    {c.message.content}
                                                                </p>
                                                            );
                                                        } else
                                                            return (
                                                                <p
                                                                    title={`response_${c.index}`}
                                                                    key={`response_${c.index}`}
                                                                >
                                                                    {c.text}
                                                                </p>
                                                            );
                                                    })}
                                                </td>
                                                <td>{tr.response.content.model}</td>
                                                <td>{tr.response.headers['content-type']}</td>
                                                <td>{tr.response.status_code}</td>
                                                <td>
                                                    {tr.response.content.usage.prompt_tokens} +{' '}
                                                    {tr.response.content.usage.completion_tokens}
                                                </td>
                                                <td>
                                                    <Link
                                                        id={tr.id}
                                                        to={`/projects/${params.projectId}/transaction/${tr.id}`}
                                                        state={{
                                                            transaction: tr,
                                                            project: {
                                                                id: data.id,
                                                                name: data.name,
                                                                api_base:
                                                                    data.ai_providers[0].api_base
                                                            }
                                                        }}
                                                    >
                                                        Details
                                                    </Link>
                                                </td>
                                            </tr>
                                        );
                                    })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </>
        );
    }
};

export default Project;
