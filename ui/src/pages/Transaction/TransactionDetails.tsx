import { Badge, Col, Flex, Row, Typography } from 'antd';
import Container from '../../components/Container/Container';
import { getTransactionResponse } from '../../api/interfaces';
import React from 'react';
import { TagsContainer } from '../../helpers/dataContainer';
import { ArrowRightOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
const { Title, Text, Link } = Typography;

interface Props {
    data: getTransactionResponse;
}

const TransactionDetails: React.FC<Props> = ({ data }) => {
    const toLocalDate = (date: string) => {
        const local = new Date(date + 'Z');
        return `${local.toLocaleDateString()} ${local.toLocaleTimeString()}`;
    };
    const navigate = useNavigate();
    const labelWidth = '119px';
    return (
        <Container>
            <Title level={2} className="h5 my-auto !mb-0">
                Transaction details
            </Title>
            <Flex vertical gap={16}>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Project:</Text>
                    </Col>
                    <Col>
                        <Link
                            onClick={() => {
                                navigate('/projects/' + data.project_id);
                            }}
                        >
                            {data.project_name}
                        </Link>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>API base:</Text>
                    </Col>
                    <Col>
                        <Text>{data.request.url}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Request time:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>{toLocalDate(data.request_time)}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Response status:</Text>
                    </Col>
                    <Col flex="auto">
                        <Badge
                            status={
                                data.status_code >= 300
                                    ? data.status_code >= 400
                                        ? 'error'
                                        : 'warning'
                                    : 'success'
                            }
                            text={data.status_code}
                        />
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Model:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>{data.model}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Response time:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>{toLocalDate(data.response_time)}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Tags:</Text>
                    </Col>
                    <Col flex="auto">
                        <TagsContainer classname="w-full" tags={data.tags} />
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Cost:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>
                            {data.status_code < 300 && data.total_cost !== null
                                ? `$ ${data.total_cost.toFixed(4)}`
                                : 'null'}
                        </Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Speed:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>{data.generation_speed}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex={labelWidth} className="text-end">
                        <Text>Tokens:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>
                            {data.status_code < 300 ? (
                                <span>
                                    {data.input_tokens} <ArrowRightOutlined /> {data.output_tokens}{' '}
                                    (Σ{' '}
                                    {data.input_tokens !== null && data.output_tokens !== null
                                        ? data.input_tokens + data.output_tokens
                                        : 'null'}
                                    )
                                </span>
                            ) : (
                                <span>null</span>
                            )}
                        </Text>
                    </Col>
                </Row>
            </Flex>
        </Container>
    );
};

export default TransactionDetails;
