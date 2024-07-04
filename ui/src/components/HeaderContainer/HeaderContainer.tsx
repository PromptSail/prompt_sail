import { Flex, Layout } from 'antd';
import outline from '../../assets/logo/symbol-teal-outline.svg';

interface Props {
    children: React.ReactNode;
    height?: number;
}

const { Header } = Layout;

const HeaderContainer: React.FC<Props> = ({ children, height = 80 }) => {
    return (
        <Header
            className={`w-full border-0 border-b border-solid border-[#F0F0F0] relative overflow-hidden`}
            style={{ height }}
        >
            <Flex className="relative h-full z-10" justify="space-between">
                {children}
            </Flex>
            <img
                src={outline}
                className="absolute right-14 opacity-60 -bottom-[70%]"
                style={{ height: height * 4.875 + 'px' }}
            />
        </Header>
    );
};

export default HeaderContainer;
