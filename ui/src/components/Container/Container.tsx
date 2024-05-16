import { Flex, Typography } from 'antd';
import { ReactNode } from 'react';
const { Title, Paragraph } = Typography;

interface Props {
    children: React.ReactNode;
    header: string | React.ReactNode;
    desc?: string | ReactNode;
    classname?: {
        parent?: string;
        title?: string;
        box?: string;
    };
}

const Container: React.FC<Props> = ({ children, header, desc, classname }) => {
    return (
        <Flex vertical gap={5} className={`${classname?.parent}`}>
            {typeof header === typeof '' && (
                <Title level={2} style={{ margin: '0 10px' }} className={`${classname?.title}`}>
                    {header}
                </Title>
            )}
            {typeof header !== typeof '' && header}
            {!!desc && <Paragraph className="ml-[10px] !mb-0">{desc}</Paragraph>}
            <div
                className={`box bg-white p-[20px] rounded-2xl flex flex-col grow border border-solid border-[#E5E5E5] ${classname?.box}`}
            >
                {children}
            </div>
        </Flex>
    );
};
export default Container;
