import { useEffect } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useGetProject } from '../api/queries';
import { getProjectResponse } from '../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from '../components/ProjectForms/UpdateProject';
import ProjectInstall from '../components/ProjectInstall/ProjectInstall';
import DeleteProject from '../components/ProjectForms/DeleteProject';
const Project: React.FC = () => {
    const navigate = useNavigate();
    const { state } = useLocation();
    const params = useParams();
    const project: UseQueryResult<AxiosResponse<getProjectResponse>> = useGetProject(
        params.projectId || ''
    );
    useEffect(() => {
        if (project.isSuccess) {
            const data = project.data.data;
            if (state !== null) {
                const transactionData = data.transactions.filter((el) => el.id == state);
                if (transactionData.length > 0) {
                    navigate(`/transaction/${state}`, {
                        state: {
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
                <div className="m-auto mb-5 mt-[100px] w-5/6 flex flex-col justify-between">
                    <div>
                        <div className="flex flex-row justify-end gap-3">
                            <DeleteProject name={data.name} projectId={params.projectId || ''} />
                            <UpdateProject
                                projectId={params.projectId || ''}
                                queryToRefetch={project}
                            />
                            <ProjectInstall
                                slug={data.slug}
                                api_base={data.ai_providers[0].api_base}
                            />
                        </div>
                        <h2 className="text-2xl font-semibold mb-2 md:text-4xl">
                            Project details:
                        </h2>
                        <div className="relative border-4 rounded border-gray-200 p-2 flex flex-col gap-3">
                            <span className="absolute right-5 top-1 text-xl font-semibold text-gray-400">
                                17 members
                            </span>
                            <p>
                                <span className="text-3xl font-semibold">{data.name}</span>
                                &nbsp;&nbsp;&nbsp;&nbsp;
                                <span className="text-xl font-semibold text-gray-400">
                                    ({`http://${data.slug}.promptsail.local`})
                                </span>
                            </p>
                            <p className="text-xl font-semibold text-gray-400">
                                <span>Total cost: $ {(Math.random() * 200 + 10).toFixed(2)}</span>
                                <span> - </span>
                                <span>{data.transactions.length} transactions</span>
                            </p>
                            <p>{data.description}</p>
                            <p className="text-2xl font-semibold">
                                {'<_DOSTAWCA_>: < LIST[_MODEL_] >'}
                            </p>
                        </div>
                    </div>
                    <div>
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
                                                        {tr.response.content.choices.map(
                                                            (c, id) => {
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
                                                            }
                                                        )}
                                                    </td>
                                                    <td>{tr.response.content.model}</td>
                                                    <td>{tr.response.headers['content-type']}</td>
                                                    <td>{tr.response.status_code}</td>
                                                    <td>
                                                        {tr.response.content.usage.prompt_tokens} +{' '}
                                                        {
                                                            tr.response.content.usage
                                                                .completion_tokens
                                                        }
                                                    </td>
                                                    <td>
                                                        <Link
                                                            id={tr.id}
                                                            to={`/transaction/${tr.id}`}
                                                            state={{
                                                                project: {
                                                                    id: data.id,
                                                                    name: data.name,
                                                                    api_base:
                                                                        data.ai_providers[0]
                                                                            .api_base
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
                </div>
            </>
        );
    }
};

export default Project;
