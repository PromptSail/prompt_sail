import { useState } from 'react';
import ProjetTile from '../../components/ProjectTile/ProjectTile';
import { getAllProjects } from '../../api/interfaces';
import { Link } from 'react-router-dom';
import { useGetAllProjects } from '../../api/queries';

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
                <div className="dashboard">
                    <div className="header">
                        <input
                            className="search-bar"
                            type="text"
                            name="search"
                            placeholder="Search"
                            onChange={(e) => {
                                const val = e.currentTarget.value;
                                if (val.length > 2) setFilter(val);
                                else if (filter != '') setFilter('');
                            }}
                        />
                    </div>
                    <div className="content">
                        <div className="projects-info">
                            <h4>Projects</h4>
                            <div className="info">
                                <span>17 members</span>
                                <span>{projects.data.length} projects</span>
                            </div>
                        </div>
                        <Link to={`/projects/add`} key="new" className="project-tile">
                            <div className="card new">
                                <h3>Add New Project +</h3>
                            </div>
                        </Link>
                        {projects.data
                            .filter((el) => filterProjects(el))
                            .map((project: getAllProjects, id: number) => (
                                <ProjetTile key={id} data={project} />
                            ))}
                    </div>
                </div>
            </>
        );
    }
};

export default Dashboard;
