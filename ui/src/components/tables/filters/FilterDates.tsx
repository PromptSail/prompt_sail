import { SetStateAction } from 'react';
import dayjs from 'dayjs';
import { TransactionsFilters } from '../../../api/types';
import { DatePicker } from 'antd';
const { RangePicker } = DatePicker;

interface Props {
    defaultValues: [string, string];
    setFilters: (args: SetStateAction<TransactionsFilters>) => void;
    // setDates: (date_from: string, date_to: string) => void;
}

const FilterDates: React.FC<Props> = ({
    defaultValues,
    setFilters
    // setDates
}) => {
    return (
        <RangePicker
            onChange={(_, dates) => {
                let dateStart = '';
                let dateEnd = '';
                if (dates[0].length > 0 && dates[1].length > 0) {
                    dateStart = new Date(dates[0]).toISOString();
                    dateEnd = new Date(dates[1]).toISOString();
                }
                setFilters((old) => ({
                    ...old,
                    date_from: dateStart,
                    date_to: dateEnd
                }));
                // setDates(dateStart, dateEnd);
            }}
            defaultValue={
                defaultValues[0].length > 1
                    ? [dayjs(defaultValues[0]), dayjs(defaultValues[1])]
                    : undefined
            }
            showTime
        />
    );
};
export default FilterDates;
