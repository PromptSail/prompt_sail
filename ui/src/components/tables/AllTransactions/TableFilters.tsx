import { Flex } from 'antd';
import { TransactionsFilters } from '../../../api/types';
import { Dispatch, SetStateAction } from 'react';
import FilterProject from '../filters/FilterProject';
import FilterDates from '../filters/FilterDates';
import FilterTags from '../filters/FilterTags';

interface Props {
    filters: TransactionsFilters;
    setFilters: Dispatch<SetStateAction<TransactionsFilters>>;
    setURLParam: (param: { [key: string]: string }) => void;
}

const TableFilters: React.FC<Props> = ({ filters, setFilters, setURLParam }) => {
    return (
        <Flex gap={10}>
            <FilterProject
                defaultValue={filters.project_id}
                setFilters={setFilters}
                setProject={(project_id: string) => {
                    setURLParam({ project_id });
                }}
            />
            <FilterDates
                defaultValues={[filters.date_from || '', filters.date_to || '']}
                setFilters={setFilters}
                // setDates={(date_from: string, date_to: string) => {
                // setURLParam({ date_from, date_to });
                // }}
            />
            <FilterTags
                defaultValue={filters.tags || ''}
                setFilters={setFilters}
                setTags={(tags: string) => {
                    setURLParam({ tags });
                }}
            />
        </Flex>
    );
};
export default TableFilters;
