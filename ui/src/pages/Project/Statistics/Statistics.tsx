import { DatePicker, Flex, Select, Typography } from 'antd';
import Container from '../Container';
import dayjs from 'dayjs';
import { Statistics_TransactionsCount } from '../../../api/types';
import { useState } from 'react';
import TransactionsCountChart from './TransactionsCountChart';
const { Title } = Typography;
const { RangePicker } = DatePicker;

interface Params {
    projectId: string;
}

const Statistics: React.FC<Params> = ({ projectId }) => {
    const [statisticsParams, setStatisticsParams] = useState<Statistics_TransactionsCount>({
        project_id: projectId
    });
    const periodOptions: Array<{
        value: Statistics_TransactionsCount['period'];
        label: Statistics_TransactionsCount['period'];
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
    return (
        <Container
            header={
                <Flex justify="space-between">
                    <Title level={2} style={{ margin: '0 10px' }}>
                        Statistics
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
                        />
                        <Select
                            options={periodOptions}
                            onChange={(val: Statistics_TransactionsCount['period']) => {
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
            <TransactionsCountChart statisticsParams={statisticsParams} />
        </Container>
    );
};

export default Statistics;
