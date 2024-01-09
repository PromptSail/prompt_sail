import TransactionsTable from '../components/tables/TransactionsTable';

const Transactions: React.FC = () => {
    return (
        <>
            <div className="p-5 px-20 pt-[100px] flex flex-col gap-5">
                <h2 className="text-2xl font-semibold mb-2 md:text-4xl">All Transactions</h2>
                <TransactionsTable />
            </div>
        </>
    );
};

export default Transactions;
