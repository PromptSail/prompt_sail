import React from 'react';
import TableWrapper from '../components/tables/AllTransactions/TableWrapper';

declare global {
    interface Window {
        test(length: number): void;
    }
}
const AllTransactions: React.FC = () => {
    return (
        <div className="p-5 px-20 gap-5">
            <h2 className="text-2xl font-semibold mb-2 md:text-4xl">All Transactions</h2>
            <div>
                <TableWrapper />
            </div>
        </div>
    );
};
export default AllTransactions;
