import { DatePicker, Flex, Select, Typography } from 'antd';
import Container from '../../../components/Container/Container';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { StatisticsParams } from '../../../api/types';
import { useRef, useState } from 'react';
import TransactionsCountChart from './TransactionsCountChart';
import TransactionsCostAndTokensChart from './TransactionsCostAndTokensChart';
import TransactionsSpeedChart from './TransactionsSpeedChart';
const { Title } = Typography;
const { RangePicker } = DatePicker;

interface Params {
    projectId: string;
}

// eslint-disable-next-line react-refresh/only-export-components
export enum Period {
    Yearly = 'year',
    Monthly = 'month',
    Weekly = 'week',
    Daily = 'day',
    Hourly = 'hour',
    Minutely = '5minutes'
}

const Statistics: React.FC<Params> = ({ projectId }) => {
    const [dates, setDates] = useState<{ start: Dayjs | null; end: Dayjs | null }>({
        start: dayjs().add(-30, 'd').startOf('day'),
        end: dayjs()
    });
    const [granularity, setGranularity] = useState<Period>(Period.Daily);
    const [statisticsParams, setStatisticsParams] = useState<StatisticsParams>({
        project_id: projectId,
        date_from: dates.start?.toISOString().substring(0, 19) || undefined,
        date_to: dates.end?.toISOString().substring(0, 19) || undefined,
        period: granularity
    });
    const rangeOKRef = useRef(false);
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
    return (
        <Container>
            <Flex justify="space-between">
                <Title level={2} className="h5 my-auto !mb-1">
                    Statistics
                </Title>
                <Flex gap={16}>
                    <RangePicker
                        maxDate={dayjs()}
                        presets={[
                            {
                                label: 'Last 30 minutes',
                                value: [dayjs().add(-0.5, 'h'), dayjs()]
                            },
                            { label: 'Last hour', value: [dayjs().add(-1, 'h'), dayjs()] },
                            { label: 'Last 6 hours', value: [dayjs().add(-6, 'h'), dayjs()] },
                            { label: 'Last 12 hours', value: [dayjs().add(-12, 'h'), dayjs()] },
                            { label: 'Today', value: [dayjs().startOf('day'), dayjs()] },
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
                        onChange={(_, dates) => {
                            if (!rangeOKRef.current) {
                                let dateStart = '';
                                let dateEnd = '';
                                if (dates[0].length > 0 && dates[1].length > 0) {
                                    dateStart = new Date(dates[0] + 'Z')
                                        .toISOString()
                                        .substring(0, 19);
                                    dateEnd = new Date(dates[1] + 'Z')
                                        .toISOString()
                                        .substring(0, 19);
                                }
                                setDates({
                                    start: dateStart.length > 0 ? dayjs(dateStart) : null,
                                    end: dateEnd.length > 0 ? dayjs(dateEnd) : null
                                });
                                setGranularityAndUpdateApi(dayjs(dateStart), dayjs(dateEnd));
                            }
                            rangeOKRef.current = false;
                        }}
                        onOk={(v) => {
                            setDates({ start: v[0], end: v[1] });
                            setGranularityAndUpdateApi(v[0], v[1]);
                            rangeOKRef.current = true;
                        }}
                        value={[dates.start, dates.end]}
                        showTime
                        allowClear={false}
                        allowEmpty={false}
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
            </Flex>
            <div>
                <TransactionsCountChart statisticsParams={statisticsParams} />
            </div>
            <div>
                <TransactionsCostAndTokensChart statisticsParams={statisticsParams} />
            </div>
            <div>
                <TransactionsSpeedChart statisticsParams={statisticsParams} />
            </div>
        </Container>
    );
};

export default Statistics;
