import { Typography, Flex, Skeleton } from 'antd';
import { TransactionsFilters } from '../api/types';
import { useEffect, useState } from 'react';
import TransactionsTable from '../components/tables/AllTransactions/TransactionsTable';
import HeaderContainer from '../components/HeaderContainer/HeaderContainer';
import Container from '../components/Container/Container';
import FilterDates from '../components/tables/filters/FilterDates';
import { useSearchParams } from 'react-router-dom';

const { Text } = Typography;

const { Title } = Typography;
const Transactions: React.FC = () => {
    const [params, setParams] = useSearchParams();
    const [filters, setFilters] = useState<TransactionsFilters>({
        project_id: params.get('project_id') || '',
        tags: params.get('tags') || '',
        date_from: params.get('date_from') || '',
        date_to: params.get('date_to') || '',
        provider_models: params.get('provider_models') || '',
        status_codes: params.get('status_codes') || '',
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
    const [transactionsCount, setTransactionsCount] = useState<number | null>(null);
    return (
        <Flex gap={24} vertical>
            <HeaderContainer>
                <div className="my-auto z-10">
                    <Title level={1} className="h4 m-auto">
                        Transactions{' '}
                        <Skeleton
                            active
                            className="inline-block w-[36px] h-[16px] translate-y-[2px]"
                            paragraph={{
                                rows: 0,
                                className: '!m-0'
                            }}
                            loading={transactionsCount === null}
                            title={{
                                width: '36px',
                                className: 'm-0'
                            }}
                        >
                            ({transactionsCount})
                        </Skeleton>
                    </Title>
                </div>
            </HeaderContainer>
            <Flex vertical gap={8} className="px-[24px]">
                <Container>
                    <Flex gap={8}>
                        <Text className="my-auto">Date:</Text>
                        <FilterDates
                            defaultValues={[filters.date_from || '', filters.date_to || '']}
                            onSetDates={(dates) => {
                                setFilters({ ...filters, date_from: dates[0], date_to: dates[1] });
                            }}
                        />
                    </Flex>
                </Container>
                <Container>
                    <div>
                        <TransactionsTable
                            filters={filters}
                            setFilters={setFilters}
                            setTransactionsCount={setTransactionsCount}
                            projectFilters
                        />
                    </div>
                </Container>
            </Flex>
        </Flex>
    );
};
export default Transactions;
