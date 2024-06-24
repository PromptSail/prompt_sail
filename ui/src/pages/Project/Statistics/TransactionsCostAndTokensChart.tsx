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
import { Flex, Segmented, Spin, Typography } from 'antd';
import { StatisticsParams } from '../../../api/types';
import { useState } from 'react';
import { customSorter, dataRounding, dateFormatter } from './formatters';
import { schemeCategory10 as colors } from 'd3-scale-chromatic';
import * as styles from '../../../styles.json';
import noData from '../../../assets/box.svg';
const { Title } = Typography;
interface Params {
    statisticsParams: StatisticsParams;
}

const TransactionsCostAndTokensChart: React.FC<Params> = ({ statisticsParams }) => {
    const TransactionsCost = useGetStatistics_TransactionsCost(statisticsParams);
    const [TokensOrCost, setTokensOrCost] = useState<'tokens' | 'cost'>('cost');
    return (
        <div className="relative flex flex-col min-h-[200px]">
            <Flex justify="space-between">
                <Title level={3} className="h5 m-0">
                    {TokensOrCost === 'tokens' ? 'Used tokens ' : 'Transactions cost '} by model
                </Title>
                <Segmented
                    options={[
                        { label: 'Cost', value: 'cost' },
                        { label: 'Tokens', value: 'tokens' }
                    ]}
                    onChange={(e: typeof TokensOrCost) => setTokensOrCost(e)}
                    value={TokensOrCost}
                    size="small"
                />
            </Flex>
            <ResponsiveContainer height={210} className="mt-4">
                {!TransactionsCost.isSuccess ? (
                    <div className="w-full h-full relative">
                        <Spin
                            size="large"
                            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                        />
                    </div>
                ) : (
                    (() => {
                        const chartData = {
                            legend: [] as string[],
                            records: [] as Record<string, number>[]
                        };
                        const data = TransactionsCost.data.data;
                        data.map((el) => {
                            const record: (typeof chartData.records)[0] = {
                                date: new Date(el.date).getTime()
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
                        return data.length < 1 ? (
                            <Flex align="center" justify="center" className="h-full" vertical>
                                <img src={noData} alt="No Data" width={150} />
                                <Title level={3}>No data</Title>
                            </Flex>
                        ) : (
                            <AreaChart
                                data={chartData.records}
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
                                    type="number"
                                    domain={(() => {
                                        const length = chartData.records.length;
                                        const diff =
                                            chartData.records[length - 1].date -
                                            chartData.records[length - 2].date;
                                        return [
                                            `dataMin - ${length % 2 == 0 ? 0 : diff}`,
                                            `dataMax + ${diff}`
                                        ];
                                    })()}
                                    scale={'time'}
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
                                    tickFormatter={
                                        TokensOrCost === 'cost'
                                            ? (v) => '$ ' + dataRounding(v, 4)
                                            : undefined
                                    }
                                    domain={[
                                        'auto',
                                        `dataMax + ${(() => {
                                            const length = chartData.records.length;
                                            const record = chartData.records[length - 1];
                                            const keys = Object.keys(record).filter((el) =>
                                                el.includes(TokensOrCost)
                                            );
                                            const values = keys.map((key) => record[key]);
                                            const max = Math.max(...values);
                                            return max / 8;
                                        })()}`
                                    ]}
                                    tick={{
                                        fill: styles.Colors.light['Text/colorTextTertiary']
                                    }}
                                    stroke={`${styles.Colors.light['Border/colorBorder']}`}
                                />
                                <Tooltip
                                    isAnimationActive={false}
                                    formatter={
                                        TokensOrCost === 'cost'
                                            ? (v) => '$ ' + dataRounding(v, 4)
                                            : undefined
                                    }
                                    itemSorter={customSorter}
                                />
                                <Legend
                                    align="left"
                                    wrapperStyle={{ marginLeft: '60px' }}
                                    formatter={(value) => (
                                        <span
                                            style={{
                                                color: styles.Colors.light['Text/colorTextBase']
                                            }}
                                        >
                                            {value}
                                        </span>
                                    )}
                                />
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
                        );
                    })()
                )}
            </ResponsiveContainer>
        </div>
    );
};

export default TransactionsCostAndTokensChart;
