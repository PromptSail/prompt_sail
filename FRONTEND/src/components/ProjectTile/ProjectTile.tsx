import { getAllProjects } from '../../api/interfaces';

interface Props {
    data: getAllProjects;
}

const ProjetTile: React.FC<Props> = ({ data }) => {
    const random = (Math.random() * 2000 + 10).toFixed(2);
    return (
        <div className="border-4 rounded border-gray-200 p-5 hover:bg-gray-100">
            <h2 className="text-2xl text-center">{data.name}</h2>
            <span>{data.description}</span>
            <ol className="mt-5" style={{ listStyle: 'inside' }}>
                <li>Members: 10</li>
                {/* <li>Transactions: {data.transactions.length}</li> */}
                <li>Experiments: 5</li>
                <li>Total cost: $ {random}</li>
            </ol>
            {/* <span>{data.slug}</span> */}
            {/* <span>{da}</span> */}
        </div>
    );
};

export default ProjetTile;
