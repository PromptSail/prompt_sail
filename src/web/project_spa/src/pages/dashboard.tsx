import { useQuery } from 'react-query';
import api from '../api/api';
import { useState } from 'react';
import ProjetTile from '../components/projectTile/projectTile';
import { getProjectResponse } from '../api/interfaces';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const [data, setData] = useState(Array<getProjectResponse>);
    const { isSuccess, isLoading, error } = useQuery('projects', () => {
        fetch('/api/api/projects', { headers: { 'Content-Type': 'application/json' } }).then(
            (res) => console.log(res)
        );
        fetch('/api/api/project/3ab7c7b3-7bf9-4e36-992b-a799c51f421b', {
            headers: { 'Content-Type': 'application/json' }
        }).then((res) => console.log(res));
        // api.getProject('3ab7c7b3-7bf9-4e36-992b-a799c51f421b')
        //     .then((res) => {
        //         console.log(res);
        //         // setData(res.data);
        //     })
        //     .catch((err) => err);
        // api.getProjects()
        //     .then((res) => {
        //         console.log(res);
        //         // setData(res.data);
        //     })
        //     .catch((err) => err);
    });

    if (isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (error)
        return (
            <>
                <div>An error has occurred</div>
                {console.log(error)}
            </>
        );
    if (isSuccess)
        return (
            <>
                <div className="w-3/4 m-auto">
                    <div className="flex flex-row justify-between">
                        <div className="flex flex-col">
                            <h2 className="text-xl font-semibold text-left">Projects</h2>
                            <div className="flex flex-row">
                                <span>17 members</span>
                                <span>30 projects</span>
                            </div>
                        </div>
                        <div className="flex flex-row gap-2">
                            <button type="button" className="btn btn-primary m-auto">
                                Search
                            </button>
                            <button type="button" className="btn btn-primary m-auto">
                                New project
                            </button>
                        </div>
                    </div>
                    <div className="grid grid-cols-1 p-5 gap-3 md:grid-cols-2">
                        {data.map((project, id) => (
                            <Link to={`/project/${project.id}`}>
                                <ProjetTile key={id} data={project} />
                            </Link>
                        ))}
                    </div>
                </div>
            </>
        );
};

export default Dashboard;
