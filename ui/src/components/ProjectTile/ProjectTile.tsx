import { Link } from 'react-router-dom';
import { getAllProjects } from '../../api/interfaces';

interface Props {
    data: getAllProjects;
}

const ProjetTile: React.FC<Props> = ({ data }) => {
    return (
        <Link to={`/projects/${data.id}`} className="project-tile">
            <div className="card">
                <h3>{data.name}</h3>
                <p className="description">{data.description}</p>
                <div className="details">
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
                </div>
            </div>
        </Link>
    );
};

export default ProjetTile;
