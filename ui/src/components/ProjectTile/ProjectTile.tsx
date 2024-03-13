import { getAllProjects } from '../../api/interfaces';
import { Card, Flex, Space, Typography } from 'antd';
import { CSSProperties } from 'react';
import { Link } from 'react-router-dom';
import { TagsContainer } from '../../helpers/dataContainer';
const { Title, Text } = Typography;

interface Props {
    data: getAllProjects;
    isListStyled: boolean;
}
const ProjectTile: React.FC<Props> = ({ isListStyled, data }) => {
    const titleStyles: CSSProperties = { margin: '0' };

    const desc = data.description;
    return (
        <Link
            to={`/projects/${data.id}`}
            style={{ gridColumn: `${isListStyled ? '1 / -1' : 'auto'}` }}
        >
            <Card hoverable styles={{ body: { padding: '16px 24px' } }}>
                {!isListStyled && (
                    <Flex vertical gap={20}>
                        <Space direction="vertical" size={1}>
                            <Title level={2} style={titleStyles}>
                                {data.name}
                            </Title>
                            <Text>{desc.length > 25 ? desc.substring(0, 25) + '...' : desc}</Text>
                        </Space>
                        <Flex vertical gap={1} style={{ fontWeight: 500 }}>
                            <Flex justify="space-between" gap={5}>
                                <Text>Members:</Text>
                                <Text>1</Text>
                            </Flex>
                            <Flex justify="space-between" gap={5}>
                                <Text>Total transactions:</Text>
                                <Text>{data.total_transactions}</Text>
                            </Flex>
                            <Flex justify="space-between" gap={5}>
                                <Text>Total cost:</Text>
                                <Text>$ 1.00</Text>
                            </Flex>
                            <Flex justify="space-between" gap={5}>
                                <Text>Tags:</Text>
                                <TagsContainer tags={data.tags} />
                            </Flex>
                        </Flex>
                    </Flex>
                )}
                {isListStyled && (
                    <Flex justify="space-between" gap={20}>
                        <Space direction="vertical" size={1}>
                            <Title level={2} style={titleStyles}>
                                {data.name}
                            </Title>
                            <Text>{desc.length > 25 ? desc.substring(0, 25) + '...' : desc}</Text>
                        </Space>
                        <Space direction="vertical">
                            <Text type="secondary">Members</Text>
                            <Title level={3} style={titleStyles}>
                                1
                            </Title>
                        </Space>
                        <Space direction="vertical">
                            <Text type="secondary">Total transactions</Text>
                            <Title level={3} style={titleStyles}>
                                {data.total_transactions}
                            </Title>
                        </Space>
                        <Space direction="vertical">
                            <Text type="secondary">Total cost</Text>
                            <Title level={3} style={titleStyles}>
                                $ 1.00
                            </Title>
                        </Space>
                        <Space direction="vertical">
                            <Text type="secondary">Tags</Text>
                            <TagsContainer tags={data.tags} />
                        </Space>
                    </Flex>
                )}
            </Card>
        </Link>
    );
};

export default ProjectTile;
