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
import { Spin, Typography } from 'antd';
import { StatisticsParams } from '../../../api/types';
import { dateFormatter } from './formatters';
import { schemeCategory10 as colors } from 'd3-scale-chromatic';
import { Segment } from 'recharts/types/cartesian/ReferenceLine';
import createTrend from 'trendline';
import React from 'react';
const { Title, Paragraph } = Typography;
interface Params {
    statisticsParams: StatisticsParams;
}

const TransactionsSpeedChart: React.FC<Params> = ({ statisticsParams }) => {
    const TransactionsSpeed = useGetStatistics_TransactionsSpeed(statisticsParams);
    if (TransactionsSpeed.isLoading) {
        return (
            <Spin
                size="large"
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
            />
        );
    }
    if (TransactionsSpeed.isSuccess) {
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
                if (rec.tokens_per_second > 0) record[`TPS_${legendName}`] = rec.tokens_per_second;
                if (rec.mean_latency > 0) record[`mean_${legendName}`] = rec.mean_latency;
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
        return (
            <div className="relative flex flex-col min-h-[200px]">
                <Paragraph className="mt-0 !mb-1 text-lg text-center font-semibold">
                    Response generation speed by model (tokens/s)
                </Paragraph>
                {data.length < 1 && (
                    <Title className="absolute top-2/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center opacity-50 z-10 !m-0">
                        No data found
                    </Title>
                )}
                {data.length > 0 && (
                    <>
                        <ResponsiveContainer width="100%" height={300}>
                            <ComposedChart
                                width={500}
                                height={400}
                                data={[...chartData.records]}
                                margin={{
                                    top: 0,
                                    right: 0,
                                    left: 0,
                                    bottom: 0
                                }}
                            >
                                <CartesianGrid stroke="#f5f5f5" />
                                <Tooltip
                                    labelFormatter={(val) => {
                                        return new Date(val).toLocaleString('en-US', {
                                            month: '2-digit',
                                            day: '2-digit',
                                            year: '2-digit'
                                        });
                                    }}
                                />
                                <Legend />

                                <XAxis
                                    dataKey="date"
                                    type="number"
                                    domain={['dataMin', 'dataMax']}
                                    scale={'time'}
                                    fontSize={12}
                                    tickFormatter={(v) => dateFormatter(v, statisticsParams.period)}
                                />
                                <YAxis type="number" width={40} />
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
                        </ResponsiveContainer>
                    </>
                )}
            </div>
        );
    }
};

export default TransactionsSpeedChart;
