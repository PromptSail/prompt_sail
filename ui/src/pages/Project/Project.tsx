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
                    <h2 className="details__header">{data.name}</h2>
                    <div className="details__content">
                        <div className="info">
                            <div className="left">
                                <div className="box">
                                    <div className="element">
                                        <span>Slug:</span>
                                        <span>{data.slug}</span>
                                    </div>
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
                                <div className="description">
                                    <h5 className="header">Description</h5>
                                    <p className="content">{data.description}</p>
                                </div>
                            </div>
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
                                <DeleteProject
                                    name={data.name}
                                    projectId={params.projectId || ''}
                                />
                            </div>
                        </div>
                        <div className="ai-providers">
                            <h5 className="header">AI Providers</h5>
                            <div className="content">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Provider</th>
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
                                                    <td>{el.deployment_name}</td>
                                                    <td>{el.provider_name}</td>
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
                <div className="tableWrapper">
                    <div className="tableWrapper__header">
                        <h5>LLM Transactions</h5>
                        <button onClick={() => navigate(`/transactions?project_id=${data.id}`)}>
                            All Project Transactions
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
