import { SetStateAction } from 'react';
import { TransactionsFilters } from '../../../api/types';

interface Props {
    pageSize: string | undefined;
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    setNewParam: (param: { [key: string]: string }) => void;
}

const FilterPageSize: React.FC<Props> = ({ pageSize, setFilters, setNewParam }) => {
    return (
        <div className="page_size">
            <select
                value={pageSize || '20'}
                onChange={(v) => {
                    const page_size = v.currentTarget.value;
                    setFilters((old) => ({
                        ...old,
                        page_size,
                        page: '1'
                    }));
                    setNewParam({ page_size });
                }}
            >
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="20">20</option>
                <option value="30">30</option>
            </select>
        </div>
    );
};
export default FilterPageSize;
