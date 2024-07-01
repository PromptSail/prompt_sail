import { Collapse, Flex, Typography } from 'antd';
import { getTransactionResponse } from '../../api/interfaces';
import Container from '../../components/Container/Container';
import { DownOutlined } from '@ant-design/icons';
import { useHandleTransactionImage } from '../../helpers/handleTransactionImage';
import React from 'react';

const { Title, Text } = Typography;

interface Props {
    data: getTransactionResponse;
}
type ContentType = string | { type: string; text?: string; image_url?: { url: string } }[];

const CollapseChild: React.FC<{ str: string }> = ({ str }) => {
    const message = useHandleTransactionImage(str);
    return <Text>{message}</Text>;
};
const CombinedContent: React.FC<{ content: ContentType }> = ({ content }) => {
    if (typeof content === 'string') {
        return <CollapseChild str={content} />;
    } else
        return (
            <Flex vertical gap={10}>
                {content.map((el, id) => {
                    const str = el.text || el.image_url?.url || 'Combined Error';
                    console.log(str);
                    return <CollapseChild key={id} str={str} />;
                })}
            </Flex>
        );
};

const Messages: React.FC<Props> = ({ data }) => {
    const collapseItems = data.messages?.map((el, id) => ({
        key: id,
        label: el.role,
        children: <CombinedContent content={el.content as ContentType} />
    })) || [
        {
            key: 0,
            label: data.error_message,
            children: ''
        }
    ];
    return (
        <Container>
            <Title level={2} className="h5 my-auto !mb-0">
                Messages details
            </Title>
            <div>
                <Collapse
                    defaultActiveKey={[`${collapseItems[collapseItems?.length - 1].key}`]}
                    expandIcon={({ isActive }) => <DownOutlined rotate={isActive ? -180 : 0} />}
                    items={collapseItems}
                />
            </div>
        </Container>
    );
};
export default Messages;
