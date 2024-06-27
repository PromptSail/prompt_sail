import { useState } from 'react';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { DatePicker, GetProps } from 'antd';
const { RangePicker } = DatePicker;
interface Props extends GetProps<typeof RangePicker> {
    defaultValues?: [string, string];
    onSetDates: (dates: [string, string]) => void;
}

const FilterDates: React.FC<Props> = ({ defaultValues, onSetDates, ...props }) => {
    let rangeOK = false;
    const [dates, setDates] = useState<[Dayjs | null, Dayjs | null]>([
        defaultValues && defaultValues[0] ? dayjs(defaultValues[0]) : null,
        defaultValues && defaultValues[1] ? dayjs(defaultValues[1]) : null
    ]);
    return (
        <RangePicker
            {...props}
            onChange={(_, dates) => {
                if (!rangeOK) {
                    let dateStart = '';
                    let dateEnd = '';
                    if (dates[0].length > 0 && dates[1].length > 0) {
                        dateStart = new Date(dates[0]).toISOString();
                        dateEnd = new Date(dates[1]).toISOString();
                    }
                    setDates(() => {
                        const start = dateStart.length ? dayjs(dates[0]) : null;
                        const end = dateEnd.length ? dayjs(dates[1]) : null;
                        onSetDates([dateStart, dateEnd]);
                        return [start, end];
                    });
                }
                rangeOK = false;
            }}
            onOk={(v) => {
                setDates(() => {
                    console.log(v);
                    onSetDates([v[0]?.toISOString() || '', v[1]?.toISOString() || '']);
                    return [v[0], v[1]];
                });
                rangeOK = true;
            }}
            value={[dates[0], dates[1]]}
            showTime
        />
    );
};
export default FilterDates;
