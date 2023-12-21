import { useEffect } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useGetProject } from '../api/queries';
import { getProjectResponse } from '../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from '../components/ProjectForms/UpdateProject';
import ProjectInstall from '../components/ProjectInstall/ProjectInstall';
import DeleteProject from '../components/ProjectForms/DeleteProject';
import LatestTransactions from '../components/tables/LatestTransactions';
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
                    navigate(`/transactions/${state}`, {
                        state: {
                            project: {
                                name: data.name,
                                api_base: data.ai_providers[0].api_base,
                                slug: data.slug
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
                <div className="p-5 px-20 pt-[100px] w-full w-5/6 h-full flex flex-col justify-between">
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
                        <LatestTransactions
                            transactions={data.transactions}
                            project={{
                                name: data.name,
                                api_base: data.ai_providers[0].api_base,
                                slug: data.slug
                            }}
                        />
                    </div>
                </div>
            </>
        );
    }
};

export default Project;
