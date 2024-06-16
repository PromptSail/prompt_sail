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
import * as styles from '../../../styles.json';
import { interpolateRdYlGn as colors } from 'd3-scale-chromatic';
const { Title } = Typography;
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
                <Title level={3} className="h5 m-0">
                    Transactions by response status
                </Title>
                {data.length < 1 && (
                    <Title
                        level={3}
                        className="h1 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0"
                    >
                        No data found
                    </Title>
                )}
                {data.length > 0 && (
                    <ResponsiveContainer height={210} className="mt-4">
                        <BarChart
                            title="Transactions count"
                            data={data}
                            margin={{
                                top: 0,
                                right: 26,
                                left: 0,
                                bottom: 0
                            }}
                        >
                            <CartesianGrid
                                strokeDasharray="0"
                                stroke={styles.Colors.light['Border/colorBorderSecondary']}
                            />
                            <XAxis
                                dataKey="date"
                                angle={0}
                                tickMargin={10}
                                tickFormatter={(v) => dateFormatter(v, statisticsParams.period)}
                                tick={{
                                    fill: styles.Colors.light['Text/colorTextTertiary'],
                                    fontWeight: 600
                                }}
                                fontSize={14}
                                height={38}
                                stroke={styles.Colors.light['Border/colorBorder']}
                            />
                            <YAxis
                                width={71}
                                allowDecimals={false}
                                tick={{
                                    fill: styles.Colors.light['Text/colorTextTertiary']
                                }}
                                stroke={`${styles.Colors.light['Border/colorBorder']}`}
                            />
                            <Tooltip itemSorter={customSorter} isAnimationActive={false} />
                            <Legend
                                align="left"
                                wrapperStyle={{ marginLeft: '60px' }}
                                formatter={(value) => (
                                    <span
                                        style={{ color: styles.Colors.light['Text/colorTextBase'] }}
                                    >
                                        {value}
                                    </span>
                                )}
                            />
                            <Bar
                                dataKey="status_200"
                                name="200 OK"
                                stackId="a"
                                fill={colors(0.9)}
                                maxBarSize={100}
                            />
                            <Bar
                                dataKey="status_300"
                                name="300 Redirection"
                                stackId="a"
                                fill={colors(0.37)}
                                maxBarSize={100}
                            />
                            <Bar
                                dataKey="status_400"
                                name="400 Client Error"
                                stackId="a"
                                fill={colors(0.25)}
                                maxBarSize={100}
                            />
                            <Bar
                                dataKey="status_500"
                                name="500 Server Error"
                                stackId="a"
                                fill={colors(0.05)}
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
