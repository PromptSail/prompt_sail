import { Collapse, Typography } from 'antd';
import { getTransactionResponse } from '../../api/interfaces';
import Container from '../../components/Container/Container';
import { DownOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

interface Props {
    data: getTransactionResponse;
}

const Messages: React.FC<Props> = ({ data }) => {
    const collapseItems = data.messages?.map((el, id) => ({
        key: id,
        label: el.role,
        children: <Text>{el.content}</Text>
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
