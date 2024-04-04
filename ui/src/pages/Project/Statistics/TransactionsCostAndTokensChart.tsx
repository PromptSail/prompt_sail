import {
    Area,
    AreaChart,
    CartesianGrid,
    Label,
    Legend,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from 'recharts';
import { useGetStatistics_TransactionsCost } from '../../../api/queries';
import { Flex, Radio, Spin, Typography } from 'antd';
import { StatisticsParams } from '../../../api/types';
import { useState } from 'react';
import { dateFormatter } from './formatters';
const { Title, Paragraph } = Typography;
interface Params {
    statisticsParams: StatisticsParams;
}

const TransactionsCostAndTokensChart: React.FC<Params> = ({ statisticsParams }) => {
    const TransactionsCost = useGetStatistics_TransactionsCost(statisticsParams);
    const [TokensOrCost, setTokensOrCost] = useState<'tokens' | 'cost'>('cost');
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
                record[`cost_${rec.model}`] = rec.total_cost;
            });

            chartData.records.push(record);
        });
        return (
            <div className="relativ flex flex-col">
                <Flex vertical>
                    <Paragraph className="mt-0 !mb-0 text-lg text-center font-semibold">
                        {TokensOrCost === 'tokens' ? 'Used tokens ' : 'Transactions cost '} by model
                    </Paragraph>
                    <Radio.Group
                        className="self-center"
                        options={[
                            { label: 'Cost', value: 'cost' },
                            { label: 'Tokens', value: 'tokens' }
                        ]}
                        onChange={(e) => setTokensOrCost(e.target.value)}
                        value={TokensOrCost}
                        optionType="button"
                    />
                </Flex>
                {data.length < 1 && (
                    <Title className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0">
                        No data found
                    </Title>
                )}
                {data.length > 0 && (
                    <>
                        <ResponsiveContainer height={200}>
                            <AreaChart
                                data={chartData.records}
                                margin={{
                                    top: 10,
                                    right: 30,
                                    left: -50,
                                    bottom: 0
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis
                                    dataKey="date"
                                    angle={0}
                                    tickMargin={10}
                                    tickFormatter={dateFormatter}
                                    fontSize={12}
                                    height={30}
                                />
                                <YAxis width={135}>
                                    <Label
                                        value={TokensOrCost === 'cost' ? 'Cost ($)' : 'Tokens'}
                                        angle={-90}
                                    />
                                </YAxis>
                                <Tooltip isAnimationActive={false} />
                                <Legend />
                                {chartData.legend.map((el) => {
                                    const random = Math.round(Math.random() * 360);
                                    return (
                                        <Area
                                            key={el}
                                            type="monotone"
                                            dataKey={`${TokensOrCost}_${el}`}
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
            </div>
        );
    }
};

export default TransactionsCostAndTokensChart;
