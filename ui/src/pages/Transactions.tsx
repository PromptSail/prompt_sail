import { Typography, Flex } from 'antd';
import { useSearchParams } from 'react-router-dom';
import { TransactionsFilters } from '../api/types';
import { useState } from 'react';
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
        page_size: params.get('page_size') || '10',
        page: params.get('page') || '1'
    });
    const setURLParam = (param: { [key: string]: string }) => {
        const newParam = new URLSearchParams(params);
        for (const key in param) {
            if (Object.prototype.hasOwnProperty.call(param, key)) {
                param[key].length > 0 ? newParam.set(key, param[key]) : newParam.delete(key);
            }
        }
        setParams(newParam);
    };
    return (
        <>
            <Title level={1} style={{ margin: 0, marginBottom: 20 }}>
                Transactions
            </Title>
            <Flex vertical gap={25}>
                <TableFilters filters={filters} setFilters={setFilters} setURLParam={setURLParam} />
                <TransactionsTable
                    filters={filters}
                    setFilters={setFilters}
                    // setURLParam={setURLParam}
                />
            </Flex>
        </>
    );
};
export default Transactions;
