import { SetStateAction } from 'react';
import dayjs from 'dayjs';
import { TransactionsFilters } from '../../../api/types';
import { DatePicker } from 'antd';
const { RangePicker } = DatePicker;

interface Props {
    defaultValues: [string, string];
    setFilters: (args: SetStateAction<TransactionsFilters>) => void;
    setDates: (date_from: string, date_to: string) => void;
}

const FilterDates: React.FC<Props> = ({ defaultValues, setFilters, setDates }) => {
    return (
        <RangePicker
            onChange={(_, dates) => {
                setFilters((old) => ({
                    ...old,
                    date_from: new Date(dates[0]).toISOString(),
                    date_to: new Date(dates[1]).toISOString()
                }));
                setDates(new Date(dates[0]).toISOString(), new Date(dates[1]).toISOString());
            }}
            defaultValue={
                defaultValues[0].length > 1
                    ? [dayjs(defaultValues[0]), dayjs(defaultValues[1])]
                    : undefined
            }
            showTime
        />
        // <DateRangePicker
        //     format="yyyy-MM-dd HH:mm:ss"
        //     placeholder="Select date range"
        //     defaultValue={(() => {
        //         if (params.get('date_from') && params.get('date_to')) {
        //             const from = new Date(`${params.get('date_from')}`);
        //             const to = new Date(`${params.get('date_to')}`);
        //             return [new Date(from.getTime()), new Date(to.getTime())];
        //         } else return null;
        //     })()}
        //     onChange={(v) => {
        //         if (v != null) {
        //             setFilters((old) => ({
        //                 ...old,
        //                 date_from: v[0].toISOString(),
        //                 date_to: v[1].toISOString(),
        //                 page: '1'
        //             }));
        //             setNewParam({
        //                 date_from: v[0].toISOString(),
        //                 date_to: v[1].toISOString()
        //             });
        //         } else {
        //             setFilters((old) => ({ ...old, date_from: '', date_to: '' }));
        //             const deleteDates = new URLSearchParams(params);
        //             deleteDates.delete('date_from');
        //             deleteDates.delete('date_to');
        //             setParams(deleteDates);
        //         }
        //     }}
        // />
    );
};
export default FilterDates;
