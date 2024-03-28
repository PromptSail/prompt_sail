import {
    Area,
    AreaChart,
    CartesianGrid,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from 'recharts';
import { useGetStatistics_TransactionsCost } from '../../../api/queries';
import { Spin, Typography } from 'antd';
import { Statistics_TransactionsCount } from '../../../api/types';
const { Title, Paragraph } = Typography;
interface Params {
    statisticsParams: Statistics_TransactionsCount;
}

const TransactionsCostChart: React.FC<Params> = ({ statisticsParams }) => {
    const TransactionsCost = useGetStatistics_TransactionsCost(statisticsParams);
    if (TransactionsCost.isLoading) {
        return (
            <Spin
                size="large"
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
            />
        );
    }
    if (TransactionsCost.isSuccess) {
        const chartData = {
            legend: [] as string[],
            records: [] as Record<string, string | number>[]
        };
        const data = TransactionsCost.data.data;
        data.map((el) => {
            const record: (typeof chartData.records)[0] = {
                date: el.date
            };

            el.records.map((rec) => {
                if (!chartData.legend.includes(rec.model)) {
                    chartData.legend.push(rec.model);
                }

                record[`tokens_${rec.model}`] =
                    rec.input_cumulative_total + rec.output_cumulative_total;
            });

            chartData.records.push(record);
        });
        return (
            <>
                {data.length < 1 && (
                    <Title className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0">
                        No data found
                    </Title>
                )}
                {data.length > 0 && (
                    <>
                        <Paragraph className="mt-2 !mb-0">Transactions cost</Paragraph>
                        <ResponsiveContainer>
                            <AreaChart
                                width={500}
                                height={400}
                                data={chartData.records}
                                margin={{
                                    top: 10,
                                    right: 30,
                                    left: 0,
                                    bottom: 0
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
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
                                <YAxis />
                                <Tooltip isAnimationActive={false} />
                                <Legend />
                                {chartData.legend.map((el) => {
                                    const random = Math.round(Math.random() * 360);
                                    console.log(random);
                                    return (
                                        <Area
                                            key={el}
                                            type="monotone"
                                            dataKey={`tokens_${el}`}
                                            name={el}
                                            stackId="1"
                                            stroke={`hsl(${random}, 100%, 40%)`}
                                            fill={`hsl(${random}, 100%, 40%)`}
                                        />
                                    );
                                })}
                            </AreaChart>
                        </ResponsiveContainer>
                    </>
                )}
            </>
        );
    }
};

export default TransactionsCostChart;
