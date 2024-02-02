import { useNavigate, useParams } from 'react-router-dom';
import { useGetTransaction } from '../api/queries';
import TransactionAndProjectDetails from '../components/TransactionAndProjectDetails/TransactionAndProjectDetails';

const Transaction: React.FC = () => {
    const params = useParams();
    const navigate = useNavigate();
    const transaction = useGetTransaction(params.transactionId || '');
    if (transaction)
        if (transaction.isLoading)
            return (
                <>
                    <div>loading...</div>
                </>
            );
    if (transaction.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transaction.error)}
                {navigate('/')}
            </>
        );
    if (transaction.isSuccess) {
        const data = transaction.data.data;
        return <TransactionAndProjectDetails transaction={data} />;
    }
};

export default Transaction;
