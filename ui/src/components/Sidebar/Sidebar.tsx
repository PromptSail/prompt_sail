import { Flex, Menu } from 'antd';
import Sider from 'antd/es/layout/Sider';
import { SetStateAction, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { checkLogin } from '../../storage/login';
import {
    HistoryOutlined,
    LeftSquareOutlined,
    LineChartOutlined,
    LogoutOutlined,
    QuestionCircleOutlined,
    RightSquareOutlined,
    RocketOutlined,
    UserOutlined
} from '@ant-design/icons';
import { ItemType, MenuItemType } from 'antd/es/menu/interface';
import Logo from '../../assets/logo/Logo-teal_white.svg';
import Symbol from '../../assets/logo/symbol-teal.svg';

interface Props {
    setLoginState: (arg: SetStateAction<boolean>) => void;
}

const Sidebar: React.FC<Props> = ({ setLoginState }) => {
    const [collapsed, setCollapsed] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();
    useEffect(() => {
        setSelectMenuItem(location.pathname);
    }, [location]);
    const itemsOnClick = (v: ItemType<MenuItemType>) => {
        const key = v?.key as string;
        if (key.charAt(0) === '/') {
            navigate(`${key}`);
        } else {
            switch (key) {
                case 'logout':
                    localStorage.removeItem('login');
                    setLoginState(checkLogin());
                    break;
                default:
                    console.log(`${key} func`);
            }
        }
    };
    const [selectedMenuItem, setSelectMenuItem] = useState(location.pathname);
    const topMenuItems: ItemType<MenuItemType>[] = [
        {
            key: '/',
            label: 'Projects',
            icon: <RocketOutlined />
        },
        {
            key: '/transactions',
            label: 'Transactions',
            icon: <HistoryOutlined />
        },
        {
            key: '/protfolio',
            label: 'Portfolio',
            icon: <LineChartOutlined />
        }
    ];
    const bottomMenuItems: ItemType<MenuItemType>[] = [
        {
            key: '/help',
            label: 'Help',
            icon: <QuestionCircleOutlined />
        },
        {
            key: '/profile',
            label: 'My profile',
            icon: <UserOutlined />
        },
        {
            key: 'logout',
            label: 'Log out',
            icon: <LogoutOutlined />,
            danger: true
        }
    ];
    return (
        <Sider
            width={272}
            collapsible
            collapsed={collapsed}
            onCollapse={setCollapsed}
            trigger={null}
        >
            <Flex justify="space-between" className="h-full" vertical>
                <Flex
                    className="w-full"
                    gap={19} // gap(19) = figma(104 - 79) - token(6)
                    vertical
                >
                    <div className="w-full border-solid border-0 border-b border-white/[.08]">
                        <img
                            src={collapsed ? Symbol : Logo}
                            height={28}
                            className="mx-[24px] my-[26px]"
                        />
                    </div>
                    <Menu
                        selectedKeys={[selectedMenuItem]}
                        mode="vertical"
                        items={topMenuItems}
                        onClick={itemsOnClick}
                    />
                </Flex>
                <Flex
                    className="w-full"
                    gap={14} // gap(14) = figma(1134 - 1109) - 2 * token(6)
                    vertical
                >
                    <Menu
                        selectedKeys={[selectedMenuItem]}
                        mode="vertical"
                        items={bottomMenuItems}
                        onClick={itemsOnClick}
                    />
                    <Menu
                        onClick={() => setCollapsed(!collapsed)}
                        className="border-solid border-0 border-t border-white/[.08] py-2"
                        mode="vertical"
                        selectable={false}
                        items={[
                            {
                                key: 'collapse',
                                label: 'Collapse',
                                icon: collapsed ? <RightSquareOutlined /> : <LeftSquareOutlined />
                            }
                        ]}
                    />
                </Flex>
            </Flex>
        </Sider>
    );
};
export default Sidebar;
