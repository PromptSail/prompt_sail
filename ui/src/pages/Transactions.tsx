import { Typography, Flex, Spin } from 'antd';
// import { useSearchParams } from 'react-router-dom';
import { TransactionsFilters } from '../api/types';
import { useEffect, useState } from 'react';
import TransactionsTable from '../components/tables/AllTransactions/TransactionsTable';
import HeaderContainer from '../components/HeaderContainer/HeaderContainer';
import { useGetAllTransactions } from '../api/queries';
import Container from '../components/Container/Container';
import FilterDates from '../components/tables/filters/FilterDates';
import { useSearchParams } from 'react-router-dom';

const { Text } = Typography;

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
    useEffect(() => {
        setURLParam(filters);
    }, [filters]);
    const transactions = useGetAllTransactions(filters);

    return (
        <Flex gap={24} vertical>
            <HeaderContainer>
                {transactions.isLoading && (
                    <Spin
                        size="large"
                        className="absolute top-1/3 left-1/2 -transtaction-x-1/2 -transtaction-y-1/3"
                    />
                )}
                {!transactions.isLoading && (
                    <div className="my-auto z-10">
                        <Title level={1} className="h4 m-auto">
                            Transactions{' '}
                            {transactions.isSuccess
                                ? `(${transactions.data.data.total_elements})`
                                : `(An error has occurred ${(
                                      <>
                                          {console.log(transactions.error)}
                                          {transactions.error?.code}
                                      </>
                                  )})`}
                        </Title>
                    </div>
                )}
            </HeaderContainer>
            <Flex vertical gap={8} className="px-[24px]">
                <Container>
                    <Flex gap={8}>
                        <Text className="my-auto">Date:</Text>
                        <FilterDates
                            defaultValues={[filters.date_from || '', filters.date_to || '']}
                            setFilters={setFilters}
                            // setDates={() => console.log('setDates')}
                        />
                    </Flex>
                </Container>
                <Container>
                    <div>
                        <TransactionsTable filters={filters} setFilters={setFilters} />
                    </div>
                </Container>
            </Flex>
        </Flex>
    );
};
export default Transactions;
