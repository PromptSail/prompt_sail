import { useQuery } from 'react-query';
import api from '../api/api';

const Dashboard = () => {
    const { data, isLoading, error } = useQuery('projects', () => {
        api.getProjects()
            .then((res) => res)
            .catch((err) => err);
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
    return (
        <>
            {console.log(data)}
            <div>data</div>
        </>
    );
};

export default Dashboard;
