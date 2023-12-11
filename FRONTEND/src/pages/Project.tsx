import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import SyntaxHighlighter from 'react-syntax-highlighter';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { Button, Modal } from 'react-bootstrap';
import { useDeleteProject, useGetProject } from '../api/queries';
import { getProjectResponse } from '../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from '../components/ProjectForms/UpdateProject';
const Project: React.FC = () => {
    const navigate = useNavigate();
    const { state } = useLocation();
    const params = useParams();
    const [isDelModalShowed, setDeleteModal] = useState(false);
    const project: UseQueryResult<AxiosResponse<getProjectResponse>> = useGetProject(
        params.projectId || ''
    );
    const deleteProject = useDeleteProject();
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
                    navigate('/');
                }
            }
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
                <div className="m-auto mb-5 mt-[100px] w-5/6">
                    <div className="flex flex-row justify-end gap-3">
                        <Button variant="primary" onClick={() => setDeleteModal((e) => !e)}>
                            Delete
                        </Button>
                        <UpdateProject
                            projectId={params.projectId || ''}
                            queryToRefetch={project}
                        />
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
                <Modal show={isDelModalShowed} onHide={() => setDeleteModal((e) => !e)}>
                    <Modal.Header closeButton>
                        <Modal.Title>Delete {data.name}</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>
                        <p>Are you sure you want to delete this project?</p>
                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="secondary" onClick={() => setDeleteModal((e) => !e)}>
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
            </>
        );
    }
};

export default Project;
