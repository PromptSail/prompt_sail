import { Flex } from 'antd';
import { ReactElement, Children, cloneElement } from 'react';

interface Props {
    children: React.ReactNode;
    classname?: string;
}

const Container: React.FC<Props> = ({ children, classname }) => {
    const renderChildren = () => {
        return Children.map(children, (child, id) => {
            let className = 'py-[16px]';
            if (id === 0) className = 'pb-[16px]';
            if (id === Children.count(children) - 1) {
                className = id === 0 ? '' : 'pt-[16px]';
            }
            return cloneElement(child as ReactElement, {
                className: `${className} px-[24px] border-0 ${
                    (child as ReactElement).props.className || ''
                }`
            });
        });
    };
    return (
        <Flex
            className={`bg-white border border-solid border-[#F0F0F0] rounded-[8px] py-[15px] divide-y divide-solid divide-[#F0F0F0] ${
                classname || ''
            }`}
            vertical
        >
            {renderChildren()}
        </Flex>
    );
};
export default Container;
