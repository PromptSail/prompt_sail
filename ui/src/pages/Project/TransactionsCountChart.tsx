import {
    Bar,
    BarChart,
    CartesianGrid,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from 'recharts';
import { useGetStatistics_TransactionsCount } from '../../api/queries';
import { useEffect, useState } from 'react';
import { getStatisticsTransactionsCount } from '../../api/interfaces';
import Container from './Container';
import { DatePicker, Flex, Select, Spin, Typography } from 'antd';
import dayjs from 'dayjs';
import { Statistics_TransactionsCount } from '../../api/types';
const { Title } = Typography;
const { RangePicker } = DatePicker;
interface Params {
    projectId: string;
}

const TransactionsCountChart: React.FC<Params> = ({ projectId }) => {
    const [statisticsParams, setStatisticsParams] = useState<Statistics_TransactionsCount>({
        project_id: projectId
    });
    const [isLoading, setLoading] = useState(true);
    const TransactionsCount = useGetStatistics_TransactionsCount(statisticsParams);
    const periodOptions: Array<{
        value: Statistics_TransactionsCount['peroid'];
        label: Statistics_TransactionsCount['peroid'];
    }> = [
        {
            value: 'minutely',
            label: 'minutely'
        },
        {
            value: 'hourly',
            label: 'hourly'
        },
        {
            value: 'daily',
            label: 'daily'
        },
        {
            value: 'weekly',
            label: 'weekly'
        },
        {
            value: 'monthly',
            label: 'monthly'
        }
    ];
    useEffect(() => {
        if (TransactionsCount.isSuccess) setData(TransactionsCount.data.data);
        console.log(statisticsParams);
        setLoading(false);
    }, [TransactionsCount.status]);
    const [data, setData] = useState<getStatisticsTransactionsCount[]>([]);

    return (
        <Container
            header={
                <Flex justify="space-between">
                    <Title level={2} style={{ margin: '0 10px' }}>
                        Counts
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
                                setLoading(true);
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
                            }}
                            showTime
                            // showHour
                            // showMinute
                        />
                        <Select
                            options={periodOptions}
                            onChange={(val: Statistics_TransactionsCount['peroid']) => {
                                setLoading(true);
                                setStatisticsParams((old) => ({ ...old, peroid: val }));
                            }}
                            defaultValue={'daily'}
                            className="w-[100px]"
                        />
                    </div>
                </Flex>
            }
            classname={{ parent: 'mt-5', box: 'relative h-[500px]' }}
        >
            {isLoading && (
                <Spin
                    size="large"
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                />
            )}
            {data.length < 1 && !isLoading && (
                <Title className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0">
                    No data found
                </Title>
            )}
            {data.length > 0 && !isLoading && (
                <ResponsiveContainer>
                    <BarChart
                        width={500}
                        height={300}
                        data={data}
                        margin={{
                            top: 0,
                            right: 0,
                            left: 0,
                            bottom: 0
                        }}
                    >
                        <CartesianGrid strokeDasharray="3" />
                        <XAxis
                            dataKey="date"
                            angle={60}
                            tickMargin={40}
                            tickFormatter={(val) => {
                                const date = new Date(val).toLocaleString('en-US', {
                                    month: 'short',
                                    day: '2-digit',
                                    year: 'numeric'
                                });
                                return `${date}`;
                            }}
                            height={100}
                        />
                        <YAxis width={40} allowDecimals={false} />
                        <Tooltip isAnimationActive={false} />
                        <Legend />
                        <Bar
                            dataKey="status_200"
                            name="200 OK"
                            stackId="a"
                            fill="#1a9850"
                            maxBarSize={100}
                        />
                        <Bar
                            dataKey="status_300"
                            name="300 Redirection"
                            stackId="a"
                            fill="#fee08b"
                            maxBarSize={100}
                        />
                        <Bar
                            dataKey="status_400"
                            name="400 Client Error"
                            stackId="a"
                            fill="#fdae61"
                            maxBarSize={100}
                        />
                        <Bar
                            dataKey="status_500"
                            name="500 Server Error"
                            stackId="a"
                            fill="#d73027"
                            maxBarSize={100}
                        />
                    </BarChart>
                </ResponsiveContainer>
            )}
        </Container>
    );
};

export default TransactionsCountChart;
