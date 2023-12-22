import { useGetAllTransactions } from '../api/queries';
import TransactionsTable from '../components/tables/TransactionsTable';

const Transactions: React.FC = () => {
    const transactions = useGetAllTransactions();
    if (transactions.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (transactions.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transactions.error)}
                {/* {navigate('/')} */}
            </>
        );
    if (transactions.isSuccess) {
        const data = transactions.data.data;
        return (
            <>
                <div className="p-5 px-20 pt-[100px] flex flex-col gap-5">
                    <h2 className="text-2xl font-semibold mb-2 md:text-4xl">All Transactions</h2>
                    <TransactionsTable
                        transactions={data}
                        project={{
                            name: '',
                            api_base: '',
                            slug: ''
                        }}
                    />
                </div>
            </>
        );
    }
};

export default Transactions;
