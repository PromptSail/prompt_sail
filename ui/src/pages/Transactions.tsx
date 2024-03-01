import { Typography, Flex } from 'antd';
import { useSearchParams } from 'react-router-dom';
import { TransactionsFilters } from '../api/types';
import { useEffect, useState } from 'react';
import { useGetAllTransactions } from '../api/queries';
import TransactionsTable from '../components/tables/AllTransactions/TransactionsTable';
import TableFilters from '../components/tables/AllTransactions/TableFilters';

const { Title } = Typography;
const Transactions = () => {
    const [params, setParams] = useSearchParams();
    const [filters, setFilters] = useState<TransactionsFilters>({
        project_id: params.get('project_id') || '',
        tags: params.get('tags') || '',
        date_from: params.get('date_from') || '',
        date_to: params.get('date_to') || '',
        page_size: params.get('page_size') || '10'
    });
    const transactions = useGetAllTransactions(filters);
    const [{ page, totalPages, totalElements }, setPagesInfo] = useState({
        page: -1,
        totalPages: -1,
        totalElements: -1
    });
    useEffect(() => {
        if (transactions.isSuccess) {
            setPagesInfo({
                page: transactions.data.data.page_index,
                totalPages: transactions.data.data.total_pages,
                totalElements: transactions.data.data.total_elements
            });
        }
    }, [transactions.status]);
    const setPage = (val: number) => {
        setFilters((old) => ({
            ...old,
            page: `${val}`
        }));
    };
    const setURLParam = (param: { [key: string]: string }) => {
        const newParam = new URLSearchParams(params);
        for (const key in param) {
            if (Object.prototype.hasOwnProperty.call(param, key)) {
                param[key].length > 0 ? newParam.set(key, param[key]) : newParam.delete(key);
            }
        }
        setParams(newParam);
    };
    if (transactions.isLoading) return <div>loading...</div>;
    if (transactions.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transactions.error)}
            </>
        );
    if (transactions.isSuccess)
        return (
            <>
                <Title level={1} style={{ margin: 0, marginBottom: 20 }}>
                    Transactions
                </Title>
                <Flex vertical gap={25}>
                    <TableFilters
                        filters={filters}
                        setFilters={setFilters}
                        setURLParam={setURLParam}
                    />
                    <TransactionsTable data={transactions.data?.data} setFilters={setFilters} />
                </Flex>
            </>
        );
};
export default Transactions;
