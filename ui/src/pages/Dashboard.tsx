import { useState } from 'react';
import ProjetTile from '../components/ProjectTile/ProjectTile';
import { getAllProjects } from '../api/interfaces';
import { Link } from 'react-router-dom';
import { Form } from 'react-bootstrap';
import { useGetAllProjects } from '../api/queries';
import AddProject from '../components/ProjectForms/AddProject';

const Dashboard = () => {
    const projects = useGetAllProjects();
    const [filter, setFilter] = useState('');
    const filterProjects = (data: getAllProjects) => {
        return (
            data.name.includes(filter) ||
            data.slug.includes(filter) ||
            data.description.includes(filter) ||
            data.tags.join(', ').includes(filter)
        );
    };
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
                {console.error(projects.error)}
            </>
        );
    if (projects.isSuccess) {
        return (
            <>
                <div>
                    <div className="flex flex-row justify-between">
                        <div className="flex flex-col">
                            <h2 className="text-3xl font-semibold text-left">Projects</h2>
                            <div className="flex flex-row gap-2">
                                <span>17 members</span>
                                <span>{projects.data.length} projects</span>
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
                            <AddProject queryToRefetch={projects} />
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
                </div>
            </>
        );
    }
};

export default Dashboard;
