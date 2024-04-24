import { getAllProjects } from '../../api/interfaces';
import { Col, Flex, Row, Typography } from 'antd';
import { Link } from 'react-router-dom';
import { TagsContainer } from '../../helpers/dataContainer';
const { Title, Text } = Typography;
interface Props {
    data: getAllProjects;
}
const ProjectTile: React.FC<Props> = ({ data }) => {
    return (
        <Link
            to={`/projects/${data.id}`}
            className={
                'relative overflow-hidden px-[24px] py-[16px] h-[82px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px] hover:border-Primary/colorPrimaryBorderHover focus:border-Primary/colorPrimaryBorderHover  focus-visible:border-Primary/colorPrimaryBorderHover focus:shadow-FocusPrimary focus-visible:shadow-FocusPrimary transition ease-in-out duration-300'
            }
        >
            <Row justify="space-between" className="flex-nowrap gap-[24px] h-full">
                <Col className="max-w-[50%] min-w-[50%] w-full">
                    <Flex vertical justify="space-between" gap={4}>
                        <Title level={2} className="h5 m-0">
                            {data.name}
                        </Title>
                        <TagsContainer tags={data.tags} />
                    </Flex>
                </Col>
                <Col className="w-full my-auto">
                    <Text>John Doe</Text>
                </Col>
                <Col className="w-full text-end my-auto">
                    <Text>{data.total_transactions}</Text>
                </Col>
                <Col className="w-full text-end my-auto">
                    <Text>{`$ ${data.total_cost.toFixed(4)}`}</Text>
                </Col>
            </Row>
            <div className="absolute top-[12px] -left-[4px] h-[32px] w-[8px] rounded-[8px] bg-Primary/colorPrimary"></div>
        </Link>
    );
};

export default ProjectTile;
