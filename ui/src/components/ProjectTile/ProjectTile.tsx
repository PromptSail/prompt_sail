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
                        <span>1</span>
                    </div>
                    <div className="element">
                        <span>Total transactions:</span>
                        <span>{data.total_transactions}</span>
                    </div>
                    <div className="element">
                        <span>Total cost:</span>
                        <span>$ 1.00</span>
                    </div>
                    <div className="element">
                        <span>Tags:</span>
                        <span>{data.tags.join(', ')}</span>
                    </div>
                </div>
            </div>
        </Link>
    );
};

export default ProjetTile;
