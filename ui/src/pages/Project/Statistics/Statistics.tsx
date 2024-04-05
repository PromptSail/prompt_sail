import { DatePicker, Flex, Select, Typography } from 'antd';
import Container from '../Container';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { StatisticsParams } from '../../../api/types';
import { useState } from 'react';
import TransactionsCountChart from './TransactionsCountChart';
import TransactionsCostAndTokensChart from './TransactionsCostAndTokensChart';
const { Title } = Typography;
const { RangePicker } = DatePicker;

interface Params {
    projectId: string;
}

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
    const [statisticsParams, setStatisticsParams] = useState<StatisticsParams>({
        project_id: projectId,
        date_from: (dates.start || dayjs().add(-30, 'd')).toISOString().substring(0, 19),
        date_to: (dates.end || dayjs()).toISOString().substring(0, 19)
    });
    const periodOptions = Object.keys(Period).map((el) => ({
        label: el,
        value: Period[el as keyof typeof Period]
    }));
    return (
        <Container
            header={
                <Flex justify="space-between">
                    <Title level={2} style={{ margin: '0 10px' }}>
                        Statistics
                    </Title>
                    <div className="mt-auto">
                        <RangePicker
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
                                setStatisticsParams((old) => ({
                                    ...old,
                                    date_from: dateStart,
                                    date_to: dateEnd
                                }));
                                setDates({
                                    start: dateStart.length > 0 ? dayjs(dateStart) : null,
                                    end: dateEnd.length > 0 ? dayjs(dateEnd) : null
                                });
                            }}
                            onOk={(v) => {
                                setDates({ start: v[0], end: v[1] });
                                setStatisticsParams((old) => ({
                                    ...old,
                                    date_from: v[0] ? v[0].toISOString().substring(0, 19) : '',
                                    date_to: v[1] ? v[1]?.toISOString().substring(0, 19) : ''
                                }));
                            }}
                            value={[dates.start, dates.end]}
                            showTime
                            allowClear={false}
                            allowEmpty={false}
                        />
                        <Select
                            options={periodOptions}
                            onChange={(val: Period) => {
                                setStatisticsParams((old) => ({ ...old, period: val }));
                            }}
                            defaultValue={Period.Daily}
                            className="w-[100px]"
                        />
                    </div>
                </Flex>
            }
            classname={{ parent: 'mt-5', box: 'relative gap-5' }}
        >
            <TransactionsCountChart statisticsParams={statisticsParams} />
            <TransactionsCostAndTokensChart statisticsParams={statisticsParams} />
        </Container>
    );
};

export default Statistics;
