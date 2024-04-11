import { Collapse, Flex, theme } from 'antd';
import { getTransactionResponse } from '../../api/interfaces';
import Container from '../Project/Container';
import { CaretRightOutlined } from '@ant-design/icons';

interface Props {
    data: getTransactionResponse;
}

const BasicInfo: React.FC<Props> = ({ data }) => {
    const { token } = theme.useToken();

    const collapseItems = data.messages?.map((el, id) => ({
        key: id,
        label: el.role,
        children: <p>{el.content}</p>,
        style: {
            background: token.colorFillAlter,
            borderRadius: token.borderRadiusLG,
            border: 'none'
        }
    })) || [
        {
            key: 0,
            label: data.error_message,
            children: '',
            style: {
                background: token.colorFillAlter,
                borderRadius: token.borderRadiusLG,
                border: 'none'
            }
        }
    ];
    return (
        <Flex vertical gap={20}>
            <Container header={'Messages'}>
                <Collapse
                    defaultActiveKey={[`${collapseItems[collapseItems?.length - 1].key}`]}
                    expandIcon={({ isActive }) => <CaretRightOutlined rotate={isActive ? 90 : 0} />}
                    items={collapseItems}
                />
            </Container>
        </Flex>
    );
};
export default BasicInfo;
