import { SetStateAction } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { SetURLSearchParams } from 'react-router-dom';
import { DateRangePicker } from 'rsuite';

interface Props {
    params: URLSearchParams;
    setParams: SetURLSearchParams;
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    setNewParam: (param: { [key: string]: string }) => void;
}

const FilterDates: React.FC<Props> = ({ params, setParams, setFilters, setNewParam }) => {
    return (
        <DateRangePicker
            format="yyyy-MM-dd HH:mm:ss"
            placeholder="Select date range"
            defaultValue={(() => {
                if (params.get('date_from') && params.get('date_to')) {
                    const from = new Date(`${params.get('date_from')}`);
                    const to = new Date(`${params.get('date_to')}`);
                    return [new Date(from.getTime()), new Date(to.getTime())];
                } else return null;
            })()}
            onChange={(v) => {
                if (v != null) {
                    setFilters((old) => ({
                        ...old,
                        date_from: v[0].toISOString(),
                        date_to: v[1].toISOString(),
                        page: '1'
                    }));
                    setNewParam({
                        date_from: v[0].toISOString(),
                        date_to: v[1].toISOString()
                    });
                } else {
                    setFilters((old) => ({ ...old, date_from: '', date_to: '' }));
                    const deleteDates = new URLSearchParams(params);
                    deleteDates.delete('date_from');
                    deleteDates.delete('date_to');
                    setParams(deleteDates);
                }
            }}
        />
    );
};
export default FilterDates;
