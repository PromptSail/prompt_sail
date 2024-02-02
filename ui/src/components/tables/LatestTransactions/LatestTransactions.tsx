import { SetStateAction, useEffect } from 'react';
import React from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllTransactions } from '../../../api/queries';
import LatestTransactionsTable from './LatestTransactionsTable';

declare global {
    interface Window {
        test(length: number): void;
    }
}
interface Props {
    projectId: string;
    lengthTransactionRequest: (length: SetStateAction<string>) => void;
}
const LatestTransactions: React.FC<Props> = ({ projectId, lengthTransactionRequest }) => {
    const filters: TransactionsFilters = {
        page_size: '5',
        project_id: projectId
    };
    const transactions = useGetAllTransactions(filters);
    useEffect(() => {
        if (transactions.isSuccess)
            lengthTransactionRequest(`${transactions.data.data.total_elements}`);
    }, [transactions.status]);

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
                <span>{transactions.error.message}</span>
            </>
        );
    if (transactions.isSuccess) {
        return <LatestTransactionsTable tableData={transactions.data.data.items} />;
    }
};
export default LatestTransactions;
