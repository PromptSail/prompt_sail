import {
    CartesianGrid,
    ComposedChart,
    Legend,
    ResponsiveContainer,
    Scatter,
    Tooltip,
    XAxis,
    YAxis,
    ReferenceLine
} from 'recharts';
import { useGetStatistics_TransactionsSpeed } from '../../../api/queries';
import { Flex, Spin, Typography } from 'antd';
import { StatisticsParams } from '../../../api/types';
import { dataRounding, dateFormatter } from './formatters';
import { schemeCategory10 as colors } from 'd3-scale-chromatic';
import { Segment } from 'recharts/types/cartesian/ReferenceLine';
import createTrend from 'trendline';
import React from 'react';
import * as styles from '../../../styles.json';
import noData from '../../../assets/box.svg';
const { Title } = Typography;
interface Params {
    statisticsParams: StatisticsParams;
}

const TransactionsSpeedChart: React.FC<Params> = ({ statisticsParams }) => {
    const TransactionsSpeed = useGetStatistics_TransactionsSpeed(statisticsParams);
    return (
        <div className="relative flex flex-col min-h-[200px]">
            <Title level={3} className="h5 m-0">
                Response generation speed by model (tokens/s)
            </Title>
            <ResponsiveContainer height={210} className="mt-4">
                {!TransactionsSpeed.isSuccess ? (
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
                        const data = TransactionsSpeed.data.data;
                        data.map((el) => {
                            const record: (typeof chartData.records)[0] = {
                                date: new Date(el.date).getTime()
                            };
                            el.records.map((rec) => {
                                const legendName = `${rec.provider.substring(0, 2)}-${rec.model}`;
                                if (!chartData.legend.includes(legendName)) {
                                    chartData.legend.push(legendName);
                                }
                                if (rec.tokens_per_second > 0)
                                    record[`TPS_${legendName}`] = rec.tokens_per_second;
                                if (rec.mean_latency > 0)
                                    record[`mean_${legendName}`] = rec.mean_latency;
                            });
                            chartData.records.push(record);
                        });
                        const trendData = (model: string): Segment[] => {
                            const modelMentions = chartData.records.filter((obj) =>
                                Object.prototype.hasOwnProperty.call(obj, `TPS_${model}`)
                            );
                            if (modelMentions.length > 1) {
                                const trend = createTrend(modelMentions, 'date', `TPS_${model}`);
                                const xMin = Math.min(...modelMentions.map((el) => el.date));
                                const xMax = Math.max(...modelMentions.map((el) => el.date));
                                const results = [
                                    { x: xMin, y: trend.calcY(xMin) },
                                    { x: xMax, y: trend.calcY(xMax) }
                                ];
                                return results;
                            } else return [];
                        };
                        return data.length < 1 ? (
                            <Flex align="center" justify="center" className="h-full" vertical>
                                <img src={noData} alt="No Data" width={150} />
                                <Title level={3}>No data</Title>
                            </Flex>
                        ) : (
                            <ComposedChart
                                data={[...chartData.records]}
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
                                <Tooltip
                                    labelFormatter={(val) => {
                                        return new Date(val).toLocaleString('en-US', {
                                            month: '2-digit',
                                            day: '2-digit',
                                            year: '2-digit'
                                        });
                                    }}
                                    formatter={(v) => dataRounding(v as number, 2)}
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
                                    type="number"
                                    width={71}
                                    domain={[
                                        0,
                                        'auto'
                                        // auto seems to work but I leave it here just in case
                                        //
                                        // (() => {
                                        //     const recordsWithMoreThanOneParam =
                                        //         chartData.records.filter(
                                        //             (el) => Object.keys(el).length > 1
                                        //         );
                                        //     const max = Math.max(
                                        //         ...recordsWithMoreThanOneParam.map((obj) => {
                                        //             const keys = Object.keys(obj).filter(
                                        //                 (key) => key !== 'date'
                                        //             );
                                        //             return Math.max(...keys.map((el) => obj[el]));
                                        //         })
                                        //     );
                                        //     const a = Number(max + max / 3).toPrecision(2);
                                        //     console.log(a);
                                        //     return Number(a);
                                        // })()
                                    ]}
                                    tick={{
                                        fill: styles.Colors.light['Text/colorTextTertiary']
                                    }}
                                    stroke={`${styles.Colors.light['Border/colorBorder']}`}
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
                                        <React.Fragment key={`speed${id}`}>
                                            <Scatter
                                                type="monotone"
                                                dataKey={`TPS_${el}`}
                                                name={el}
                                                stroke={colors[id % colors.length]}
                                                fill={colors[id % colors.length]}
                                            />
                                            <ReferenceLine
                                                stroke={colors[id % colors.length]}
                                                strokeDasharray="3 3"
                                                strokeWidth={3}
                                                segment={trendData(el)}
                                            />
                                        </React.Fragment>
                                    );
                                })}
                            </ComposedChart>
                        );
                    })()
                )}
            </ResponsiveContainer>
        </div>
    );
};

export default TransactionsSpeedChart;
