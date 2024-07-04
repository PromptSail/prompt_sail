import { useState } from 'react';
import { getProjectResponse } from '../../api/interfaces';
import { TransactionsFilters } from '../../api/types';
import Container from '../../components/Container/Container';
import FilterDates from '../../components/tables/filters/FilterDates';
import TransactionsTable from '../../components/tables/AllTransactions/TransactionsTable';
import { Flex, Typography } from 'antd';

const { Text } = Typography;
interface Props {
    projectId: getProjectResponse['id'];
}

const ProjectTransactions: React.FC<Props> = ({ projectId }) => {
    const [filters, setFilters] = useState<TransactionsFilters>({ project_id: projectId });
    return (
        <>
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
                    <TransactionsTable filters={filters} setFilters={setFilters} />
                </div>
            </Container>
        </>
    );
};

export default ProjectTransactions;
