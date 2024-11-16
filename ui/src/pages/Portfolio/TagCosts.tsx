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
import { Flex, Spin, Typography } from 'antd';
import { customSorter, dataRounding, dateFormatter } from '../Project/Statistics/formatters';
import noData from '../../assets/box.svg';
import * as styles from '../../styles.json';
import { schemeCategory10 as colors } from 'd3-scale-chromatic';
import { StatisticsParams } from '../../api/types';
import { useGetTagsUsage } from '../../api/queries';
const { Title } = Typography;

const TagCosts: React.FC<{ dateParams: Omit<StatisticsParams, 'project_id'> }> = ({
    dateParams
}) => {
    const tags = useGetTagsUsage(dateParams);
    return (
        <>
            <Title level={2} className="h5 m-0">
                Tags costs
            </Title>
            <ResponsiveContainer height={210} className="mt-4">
                {tags.isLoading ? (
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

                        tags.data?.map(
                            (el: {
                                date: string;
                                records: {
                                    tag: string;
                                    total_cost: number;
                                }[];
                            }) => {
                                const record: (typeof chartData.records)[0] = {
                                    date: new Date(el.date).getTime()
                                };

                                el.records.map((rec) => {
                                    const legendName = `${rec.tag}`;
                                    if (!chartData.legend.includes(legendName)) {
                                        chartData.legend.push(legendName);
                                    }
                                    record[`cost_${legendName}`] = rec.total_cost;
                                });

                                chartData.records.push(record);
                            }
                        );
                        return chartData.records.length < 1 ? (
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
                                    tickFormatter={(v) => dateFormatter(v, dateParams.period)}
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
                                    tickFormatter={(v) => '$ ' + dataRounding(v, 4)}
                                    domain={[
                                        'auto',
                                        `dataMax + ${(() => {
                                            const length = chartData.records.length;
                                            const record = chartData.records[length - 1];
                                            const keys = Object.keys(record).filter((el) =>
                                                el.includes('cost')
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
                                    formatter={(v) => '$ ' + dataRounding(v, 4)}
                                    labelFormatter={(label) => {
                                        return new Date(label).toLocaleString();
                                    }}
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
                                            dataKey={`cost_${el}`}
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
        </>
    );
};

export default TagCosts;
