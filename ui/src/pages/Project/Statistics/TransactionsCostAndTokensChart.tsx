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
import { Flex, Radio, Spin, Typography } from 'antd';
import { StatisticsParams } from '../../../api/types';
import { useState } from 'react';
import { costFormatter, costTooltip, customSorter, dateFormatter } from './formatters';
import { schemeCategory10 as colors } from 'd3-scale-chromatic';
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
                const legendName = `${rec.provider.substring(0, 2)}-${rec.model}`;
                if (!chartData.legend.includes(legendName)) {
                    chartData.legend.push(legendName);
                }
                record[`tokens_${legendName}`] =
                    rec.input_cumulative_total + rec.output_cumulative_total;
                record[`cost_${legendName}`] = rec.total_cost;
            });

            chartData.records.push(record);
        });
        return (
            <div className="relative flex flex-col min-h-[200px]">
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
                    <Title className="absolute top-2/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0">
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
                                <YAxis
                                    width={110}
                                    tickFormatter={
                                        TokensOrCost === 'cost' ? costFormatter : undefined
                                    }
                                />
                                <Tooltip
                                    isAnimationActive={false}
                                    formatter={TokensOrCost === 'cost' ? costTooltip : undefined}
                                    itemSorter={customSorter}
                                />
                                <Legend />
                                {chartData.legend.map((el, id) => {
                                    return (
                                        <Area
                                            key={el}
                                            type="monotone"
                                            dataKey={`${TokensOrCost}_${el}`}
                                            name={el}
                                            stackId="1"
                                            stroke={colors[id % colors.length]}
                                            fill={colors[id % colors.length]}
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
