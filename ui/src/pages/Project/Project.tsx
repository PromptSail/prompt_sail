import { useNavigate, useParams } from 'react-router-dom';
import { useGetProject } from '../../api/queries';
import { getProjectResponse } from '../../api/interfaces';
import { AxiosResponse } from 'axios';
import { UseQueryResult } from 'react-query';
import UpdateProject from '../../components/ProjectForms/UpdateProject';
import ProjectInstall from '../../components/ProjectInstall/ProjectInstall';
import DeleteProject from '../../components/ProjectForms/DeleteProject';
import LatestTransactions from '../../components/tables/LatestTransactions/LatestTransactions';
import { OverlayTrigger, Popover } from 'react-bootstrap';
import AddProject from '../../components/ProjectForms/AddProject';
import { makeUrl } from '../../helpers/aiProvider';
const Project: React.FC & { Add: React.FC; Update: React.FC } = () => {
    const navigate = useNavigate();
    const params = useParams();
    const project: UseQueryResult<AxiosResponse<getProjectResponse>> = useGetProject(
        params.projectId || ''
    );
    const popover = (description: string) => (
        <Popover>
            <Popover.Header>Description</Popover.Header>
            <Popover.Body>{description}</Popover.Body>
        </Popover>
    );
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
            <div className="project">
                <div className="details">
                    <div className="details__header">
                        <h2>{data.name}</h2>
                        <div className="buttons">
                            <ProjectInstall
                                slug={data.slug}
                                api_base={data.ai_providers[0].api_base}
                            />
                            <button
                                onClick={() =>
                                    navigate(`/projects/${params.projectId}/update`, {
                                        state: { project: data }
                                    })
                                }
                            >
                                Edit
                            </button>
                            <DeleteProject name={data.name} projectId={params.projectId || ''} />
                        </div>
                    </div>
                    <div className="description">
                        <p className="content">{data.description}</p>
                    </div>
                    <div className="details__content">
                        <div className="box basicInfo">
                            <h5 className="header">Basic info</h5>
                            <div className="content">
                                <div className="element">
                                    <span>Members:</span>
                                    <span>10</span>
                                </div>
                                <div className="element">
                                    <span>Total tranasction:</span>
                                    <span>{data.total_transactions}</span>
                                </div>
                                <div className="element">
                                    <span>Total const:</span>
                                    <span>$ 129.32</span>
                                </div>
                                <div className="element">
                                    <span>Tags:</span>
                                    <span>{data.tags.join(', ')}</span>
                                </div>
                            </div>
                        </div>
                        <div className="box aiProviders">
                            <h5 className="header">AI Providers</h5>
                            <div className="content">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Provider</th>
                                            <th>Deployment name</th>
                                            <th>Proxy url</th>
                                            <th>Api base url</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {data.ai_providers.map((el, id) => (
                                            <OverlayTrigger
                                                placement="bottom"
                                                key={id}
                                                overlay={
                                                    el.description.length > 1 ? (
                                                        popover(el.description)
                                                    ) : (
                                                        <></>
                                                    )
                                                }
                                            >
                                                <tr>
                                                    <td>{el.provider_name}</td>
                                                    <td>{el.deployment_name}</td>
                                                    <td>{makeUrl(data.slug, el.slug)}</td>
                                                    <td>{el.api_base}</td>
                                                </tr>
                                            </OverlayTrigger>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="box tableWrapper">
                    <div className="header">
                        <h5>LLM Transactions</h5>
                        <button onClick={() => navigate(`/transactions?project_id=${data.id}`)}>
                            View all Transactions
                        </button>
                    </div>
                    <div className="content">
                        <LatestTransactions projectId={data.id} />
                    </div>
                </div>
            </div>
        );
    }
};
Project.Add = AddProject;
Project.Update = UpdateProject;

export default Project;
