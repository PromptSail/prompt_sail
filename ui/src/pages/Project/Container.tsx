import { Flex, Typography } from 'antd';
import { CSSProperties } from 'react';
const { Title } = Typography;

interface Props {
    children: React.ReactNode;
    header: string;
    classname?: string;
}

const Container: React.FC<Props> = ({ children, header, classname }) => {
    const style: CSSProperties = {
        background: '#FFF',
        padding: '20px',
        borderRadius: '15px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        gap: '10px',
        flexGrow: '1',
        border: '1px solid #E5E5E5'
    };
    return (
        <Flex className={classname} vertical gap={5}>
            <Title level={2} style={{ margin: '0 10px' }}>
                {header}
            </Title>
            <div className="container" style={style}>
                {children}
            </div>
        </Flex>
    );
};
export default Container;
