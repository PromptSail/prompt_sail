import { getProjectResponse } from '../../api/interfaces';

interface Props {
    data: getProjectResponse;
}

const ProjetTile: React.FC<Props> = ({ data }) => {
    return (
        <div className="border-4 rounded border-gray-400">
            <span>{data.name}</span>
            {/* <span>{data.slug}</span> */}
            {/* <span>{data.description}</span> */}
            {/* <span>{da}</span> */}
        </div>
    );
};

export default ProjetTile;
