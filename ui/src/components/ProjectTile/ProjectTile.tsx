import { Link } from 'react-router-dom';
import { getAllProjects } from '../../api/interfaces';

interface Props {
    data: getAllProjects;
}

const ProjetTile: React.FC<Props> = ({ data }) => {
    const tags = data.tags.join(', ');
    const desc = data.description;
    return (
        <Link to={`/projects/${data.id}`} className="project-tile">
            <div className="card">
                <h3>{data.name}</h3>
                <p className="description">
                    {desc.length > 25 ? desc.substring(0, 25) + '...' : desc}
                </p>
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
                        <span>{tags.length > 20 ? tags.substring(0, 20) + '...' : tags}</span>
                    </div>
                </div>
            </div>
        </Link>
    );
};

export default ProjetTile;
