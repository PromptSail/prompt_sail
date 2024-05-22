import { Button, Col, Collapse, CollapseProps, Divider, Flex, Row, Typography, theme } from 'antd';
import { getProjectResponse } from '../../api/interfaces';
import { makeUrl } from '../../helpers/aiProvider';
import { DeleteOutlined, DownOutlined, EditOutlined, FileAddOutlined } from '@ant-design/icons';
import { useState } from 'react';
import { CollapsibleType } from 'antd/es/collapse/CollapsePanel';
const { Text, Title } = Typography;

interface Props {
    list: getProjectResponse['ai_providers'];
    slug: getProjectResponse['slug'];
}

const AiProvidersList: React.FC<Props> = ({ list, slug }) => {
    const { token } = theme.useToken();
    const [collapseTrigger, setcollapseTrigger] = useState<CollapsibleType>('header');
    const items: CollapseProps['items'] = list.map((el, item_id) => ({
        key: item_id,
        label: (
            <Flex justify="space-between">
                <Title level={2} className="h5 m-0 lh-0">
                    {el.deployment_name}
                </Title>
                <Flex gap={12}>
                    <Button
                        icon={<EditOutlined />}
                        size="small"
                        type="text"
                        onMouseEnter={() => setcollapseTrigger('icon')}
                        onMouseLeave={() => setcollapseTrigger('header')}
                    >
                        Edit
                    </Button>
                    <Button
                        icon={<DeleteOutlined />}
                        size="small"
                        type="text"
                        onMouseEnter={() => setcollapseTrigger('icon')}
                        onMouseLeave={() => setcollapseTrigger('header')}
                    />
                    <Divider type="vertical" className="h-full m-0" />
                </Flex>
            </Flex>
        ),
        style: {
            background: token.colorBgContainer,
            // @ts-expect-error token.Collapse.colorBorder is correctly defined in /ui/src/theme-light.tsx
            border: `1px solid ${token.Collapse.colorBorder}`,
            borderRadius: '8px'
        },
        children: (
            <Flex vertical gap={16}>
                <Row gutter={12}>
                    <Col flex="129px" className="text-end">
                        <Text>AI Provider:</Text>
                    </Col>
                    <Col>
                        <Text>{el.provider_name}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex="129px" className="text-end">
                        <Text className="!m-0">Deployment name:</Text>
                    </Col>
                    <Col>
                        <Text>{el.deployment_name}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex="129px" className="text-end">
                        <Text>API base URL:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>{el.api_base}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex="129px" className="text-end">
                        <Text>Proxy URL:</Text>
                    </Col>
                    <Col flex="auto">
                        <Text>{makeUrl(slug, el.deployment_name)}</Text>
                    </Col>
                </Row>
                <Row gutter={12}>
                    <Col flex="129px" className="text-end"></Col>
                    <Col flex="auto">
                        <Button size="small" icon={<FileAddOutlined />}>
                            Proxy URL Configuration
                        </Button>
                    </Col>
                </Row>
            </Flex>
        )
    }));
    return (
        <>
            <Collapse
                collapsible={collapseTrigger}
                defaultActiveKey={items.length < 4 ? items.map((_el, id) => id) : []}
                style={{
                    background: token.Layout?.bodyBg,
                    border: 'none',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 12,
                    padding: 0
                }}
                expandIcon={({ isActive }) => (
                    <DownOutlined className="my-auto !text-[14px]" rotate={isActive ? 180 : 0} />
                )}
                expandIconPosition="end"
                items={items}
            />
        </>
    );
};
export default AiProvidersList;
