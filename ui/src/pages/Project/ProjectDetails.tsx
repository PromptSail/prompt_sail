import { Button, Col, Flex, Row, Typography } from 'antd';
import Container from '../../components/Container/Container';
import { EditOutlined } from '@ant-design/icons';
import { getProjectResponse } from '../../api/interfaces';
import { TagsContainer } from '../../helpers/dataContainer';
const { Title, Paragraph, Text } = Typography;

interface Props {
    details: getProjectResponse;
}

const ProjectDetails: React.FC<Props> = ({ details }) => (
    <>
        <Container classname={'mt-[24px]'}>
            <Flex justify="space-between">
                <Title level={2} className="h5 my-auto !mb-1">
                    Project details
                </Title>
                <Button type="text" size="small" icon={<EditOutlined />}>
                    Edit
                </Button>
            </Flex>
            <Flex vertical gap={16}>
                <Row gutter={12}>
                    <Col flex="100px" className="text-end">
                        <Text>Owner:</Text>
                    </Col>
                    <Col>
                        <Text>{details.name}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex="100px" className="text-end">
                        <Text>Description:</Text>
                    </Col>
                    <Col>
                        <Text>{details.description}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex="100px" className="text-end">
                        <Text>Tags:</Text>
                    </Col>
                    <Col flex="auto">
                        <TagsContainer classname="w-full" tags={details.tags} />
                    </Col>
                </Row>
            </Flex>
        </Container>
        <Container>
            <Flex className="divide-x divide-solid divide-[#F0F0F0]">
                <div className="border-0 pe-[24px]">
                    <Paragraph className="!mb-1 text-Text/colorTextDescription">
                        Total transactions
                    </Paragraph>
                    <Text className="text-Text/colorText">{details.total_transactions}</Text>
                </div>
                <div className="border-0 ps-[24px]">
                    <Paragraph className="!mb-1 text-Text/colorTextDescription">
                        Total cost
                    </Paragraph>
                    <Text className="text-Text/colorText">{details.total_cost}</Text>
                </div>
            </Flex>
        </Container>
    </>
);
export default ProjectDetails;
