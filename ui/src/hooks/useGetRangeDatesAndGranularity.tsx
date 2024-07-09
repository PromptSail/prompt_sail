import { useState } from 'react';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { StatisticsParams } from '../api/types';
import { Flex, Select } from 'antd';
import FilterDates from '../components/tables/filters/FilterDates';

// eslint-disable-next-line react-refresh/only-export-components
export enum Period {
    Yearly = 'year',
    Monthly = 'month',
    Weekly = 'week',
    Daily = 'day',
    Hourly = 'hour',
    Minutely = '5minutes'
}

const useGetRangeDatesAndGranularity = (
    defaults = {
        dateStart: dayjs().add(-1, 'w').startOf('day'),
        dateEnd: dayjs(),
        granularity: Period.Daily
    }
) => {
    const [dates, setDates] = useState<{ start: Dayjs | null; end: Dayjs | null }>({
        start: defaults.dateStart,
        end: defaults.dateEnd
    });
    const [granularity, setGranularity] = useState<Period>(defaults.granularity);
    const [statisticsParams, setStatisticsParams] = useState<Omit<StatisticsParams, 'project_id'>>({
        date_from: dates.start?.toISOString().substring(0, 19) || undefined,
        date_to: dates.end?.toISOString().substring(0, 19) || undefined,
        period: granularity
    });
    const getEnablePeriodOptions = (start: Dayjs | null, end: Dayjs | null) => {
        const options: Array<Period> = [];
        if (start == null || end == null) return options;
        else {
            Object.keys(Period).map((_, id) => {
                switch (id) {
                    case 0: // year
                        if (end.diff(start, 'y', true) >= 1) options.push(Period.Yearly);
                        break;
                    case 1: // month
                        if (end.diff(start, 'M', true) >= 1 && end.diff(start, 'y', true) <= 2)
                            options.push(Period.Monthly);
                        break;
                    case 2: // week
                        if (end.diff(start, 'w', true) >= 1 && end.diff(start, 'M', true) <= 12)
                            options.push(Period.Weekly);
                        break;
                    case 3: // day
                        if (end.diff(start, 'd', true) >= 1 && end.diff(start, 'M', true) <= 2)
                            options.push(Period.Daily);
                        break;
                    case 4: // hour
                        if (end.diff(start, 'h', true) >= 1 && end.diff(start, 'h', true) <= 60)
                            options.push(Period.Hourly);
                        break;
                    case 5: // minutes
                        if (end.diff(start, 'h', true) <= 5) options.push(Period.Minutely);
                        break;
                    default:
                        break;
                }
            });
            return options;
        }
    };
    const enablePeriod = getEnablePeriodOptions(dates.start, dates.end);
    const periodOptions = Object.keys(Period).map((el) => {
        return {
            label: el,
            value: Period[el as keyof typeof Period],
            disabled:
                enablePeriod.length > 0
                    ? enablePeriod.includes(Period[el as keyof typeof Period])
                        ? false
                        : true
                    : true
        };
    });
    const setGranularityAndUpdateApi = (start: Dayjs | null, end: Dayjs | null) => {
        const enablePeriod = getEnablePeriodOptions(start, end);
        const properGranularity = enablePeriod.includes(granularity)
            ? granularity
            : enablePeriod[0];
        setGranularity(properGranularity);
        setStatisticsParams((old) => ({
            ...old,
            date_from: start ? start.toISOString().substring(0, 19) : '',
            date_to: end ? end?.toISOString().substring(0, 19) : '',
            period: properGranularity || Period.Daily
        }));
    };

    return {
        params: statisticsParams,
        RangeAndGranularity: (
            <Flex gap={16}>
                <FilterDates
                    defaultValues={[
                        dates.start?.toISOString() || '',
                        dates.end?.toISOString() || ''
                    ]}
                    onSetDates={(dates) => {
                        setDates({
                            start: dates.length > 0 ? dayjs(dates[0]) : null,
                            end: dates.length > 0 ? dayjs(dates[1]) : null
                        });
                        setGranularityAndUpdateApi(dayjs(dates[0]), dayjs(dates[1]));
                    }}
                    maxDate={dayjs()}
                    allowClear={false}
                    allowEmpty={false}
                    presets={[
                        {
                            label: 'Last 30 minutes',
                            value: [dayjs().add(-0.5, 'h'), dayjs()]
                        },
                        {
                            label: 'Last hour',
                            value: [dayjs().add(-1, 'h'), dayjs()]
                        },
                        {
                            label: 'Last 6 hours',
                            value: [dayjs().add(-6, 'h'), dayjs()]
                        },
                        {
                            label: 'Last 12 hours',
                            value: [dayjs().add(-12, 'h'), dayjs()]
                        },
                        {
                            label: 'Today',
                            value: [dayjs().startOf('day'), dayjs()]
                        },
                        {
                            label: 'Yesterday',
                            value: [
                                dayjs().add(-1, 'd').startOf('day'),
                                dayjs().add(-1, 'd').endOf('day')
                            ]
                        },
                        {
                            label: 'Last 7 Days',
                            value: [dayjs().add(-7, 'd').startOf('day'), dayjs()]
                        },
                        {
                            label: 'Last 14 Days',
                            value: [dayjs().add(-14, 'd').startOf('day'), dayjs()]
                        },
                        {
                            label: 'Last 30 Days',
                            value: [dayjs().add(-30, 'd').startOf('day'), dayjs()]
                        }
                    ]}
                />
                <Select
                    options={periodOptions}
                    value={granularity}
                    onChange={(val: Period) => {
                        setGranularity(val);
                        setStatisticsParams((old) => ({ ...old, period: val }));
                    }}
                    defaultValue={Period.Daily}
                    className="w-[100px]"
                />
            </Flex>
        )
    };
};

export default useGetRangeDatesAndGranularity;
