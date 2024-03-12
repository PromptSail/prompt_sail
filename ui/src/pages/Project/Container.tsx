import { Flex, Typography } from 'antd';
import { ReactNode } from 'react';
const { Title, Paragraph } = Typography;

interface Props {
    children: React.ReactNode;
    header: string;
    desc?: string | ReactNode;
    classname?: string;
}

const Container: React.FC<Props> = ({ children, header, desc, classname }) => {
    return (
        <Flex vertical gap={5}>
            <Title level={2} style={{ margin: '0 10px' }}>
                {header}
            </Title>
            {!!desc && <Paragraph className="ml-[10px] !mb-0">{desc}</Paragraph>}
            <div
                className={`container bg-white p-[20px] rounded-2xl d-flex flex-col justify-between gap-2.5 grow border border-solid border-[#E5E5E5] ${classname}`}
            >
                {children}
            </div>
        </Flex>
    );
};
export default Container;
