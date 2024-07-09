import { Flex, Typography } from 'antd';
import Container from '../../../components/Container/Container';
import TransactionsCountChart from './TransactionsCountChart';
import TransactionsCostAndTokensChart from './TransactionsCostAndTokensChart';
import TransactionsSpeedChart from './TransactionsSpeedChart';
import useGetRangeDatesAndGranularity from '../../../hooks/useGetRangeDatesAndGranularity';
const { Title } = Typography;

interface Params {
    projectId: string;
}

const Statistics: React.FC<Params> = ({ projectId }) => {
    const { params, RangeAndGranularity } = useGetRangeDatesAndGranularity();
    return (
        <Container>
            <Flex justify="space-between">
                <Title level={2} className="h5 my-auto !mb-1">
                    Statistics
                </Title>
                {RangeAndGranularity}
            </Flex>
            <div>
                <TransactionsCountChart statisticsParams={{ project_id: projectId, ...params }} />
            </div>
            <div>
                <TransactionsCostAndTokensChart
                    statisticsParams={{ project_id: projectId, ...params }}
                />
            </div>
            <div>
                <TransactionsSpeedChart statisticsParams={{ project_id: projectId, ...params }} />
            </div>
        </Container>
    );
};

export default Statistics;
