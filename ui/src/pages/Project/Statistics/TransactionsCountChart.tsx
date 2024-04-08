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
import { useGetStatistics_TransactionsCount } from '../../../api/queries';
import { Spin, Typography } from 'antd';
import { StatisticsParams } from '../../../api/types';
import { customSorter, dateFormatter } from './formatters';
const { Title, Paragraph } = Typography;
interface Params {
    statisticsParams: StatisticsParams;
}

const TransactionsCountChart: React.FC<Params> = ({ statisticsParams }) => {
    const TransactionsCount = useGetStatistics_TransactionsCount(statisticsParams);
    if (TransactionsCount.isLoading) {
        return (
            <Spin
                size="large"
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
            />
        );
    }
    if (TransactionsCount.isSuccess) {
        const data = TransactionsCount.data.data;
        return (
            <div className="relative flex flex-col min-h-[200px]">
                <Paragraph className="mt-0 !mb-1 text-lg text-center font-semibold">
                    Transactions by response status
                </Paragraph>
                {data.length < 1 && (
                    <Title className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0">
                        No data found
                    </Title>
                )}
                {data.length > 0 && (
                    <ResponsiveContainer height={200}>
                        <BarChart
                            title="Transactions count"
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
                                angle={0}
                                tickMargin={10}
                                tickFormatter={dateFormatter}
                                fontSize={12}
                                height={30}
                            />
                            <YAxis width={40} allowDecimals={false} />
                            <Tooltip itemSorter={customSorter} isAnimationActive={false} />
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
            </div>
        );
    }
};

export default TransactionsCountChart;
