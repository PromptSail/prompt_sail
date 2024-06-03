import { Divider, Flex, Menu, Skeleton, Tooltip, Typography } from 'antd';
import Sider from 'antd/es/layout/Sider';
import { SetStateAction, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { checkLogin } from '../../storage/login';
import {
    HistoryOutlined,
    LeftSquareOutlined,
    // LineChartOutlined,
    LogoutOutlined,
    QuestionCircleOutlined,
    RightSquareOutlined,
    RocketOutlined
    // UserOutlined
} from '@ant-design/icons';
import { ItemType, MenuItemType } from 'antd/es/menu/interface';
import Logo from '../../assets/logo/Logo-teal_white.svg';
import Symbol from '../../assets/logo/symbol-teal.svg';
import { useGetConfig, useWhoami } from '../../api/queries';
import defAvatar from '../../assets/logo/symbol-teal.svg';
const { Text } = Typography;
interface Props {
    setLoginState: (arg: SetStateAction<boolean>) => void;
}

const Sidebar: React.FC<Props> = ({ setLoginState }) => {
    const [collapsed, setCollapsed] = useState(false);
    const location = useLocation();
    const user = useWhoami();
    const config = useGetConfig();
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
                    localStorage.removeItem('PS_TOKEN');
                    setLoginState(checkLogin());
                    break;
                case 'help':
                    window.open('https://promptsail.com/', '_blank');
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
            key: 'divider',
            label: <Divider className="bg-white/[.08] my-[20px]" />,
            disabled: true,
            className: '!cursor-default !p-0'
        },
        {
            key: 'help',
            label: 'Help',
            icon: <QuestionCircleOutlined />
        }
        // {
        //     key: '/protfolio',
        //     label: 'Portfolio',
        //     icon: <LineChartOutlined />
        // }
    ];
    const bottomMenuItems: ItemType<MenuItemType>[] = [
        {
            key: 'logout',
            label: 'Log out',
            icon: <LogoutOutlined />
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
                    <div className="border border-solid border-white/[.08] rounded-[8px] p-[8px] mx-[16px]">
                        <Flex gap={8}>
                            {user.isLoading && (
                                <Skeleton.Avatar
                                    active
                                    shape="circle"
                                    size={'large'}
                                    style={{
                                        filter: 'brightness(.1) invert(1)'
                                    }}
                                />
                            )}
                            {!user.isLoading &&
                                (() => {
                                    const isPictureValid =
                                        user.isSuccess && user.data?.data.picture.length > 0;
                                    return (
                                        <Tooltip
                                            placement="right"
                                            title={
                                                collapsed ? (
                                                    <Flex vertical>
                                                        <Text className="text-Text/colorTextLight">
                                                            {user.data?.data.email}
                                                        </Text>
                                                        <Text className="text-Text/colorTextQuaternary font-[12px] leading-5">
                                                            {config.data?.data.organization}
                                                        </Text>
                                                    </Flex>
                                                ) : (
                                                    false
                                                )
                                            }
                                        >
                                            <img
                                                src={
                                                    isPictureValid
                                                        ? user.data?.data.picture
                                                        : defAvatar
                                                }
                                                className={`max-w-[32px] max-h-[32px] my-auto${
                                                    isPictureValid ? ' rounded-[50%]' : ''
                                                }`}
                                                alt="avatar"
                                            />
                                        </Tooltip>
                                    );
                                })()}
                            {!collapsed && (
                                <Flex vertical className="min-w-[100px]">
                                    <Text className="text-Text/colorTextLight">
                                        <Skeleton
                                            active
                                            paragraph={{
                                                rows: 0,
                                                className: '!m-0 '
                                            }}
                                            loading={user.isLoading}
                                            title={{
                                                width: '100%',
                                                className:
                                                    'm-0 mt-[6px] !bg-gradient-to-r from-Text/colorTextLight/[.30] from-25% via-Text/colorTextLight/[.50] via-37% to-Text/colorTextLight/[.30] to-63%'
                                            }}
                                        >
                                            {user.data?.data.email}
                                        </Skeleton>
                                    </Text>

                                    <Text className="text-Text/colorTextQuaternary font-[12px] leading-5">
                                        <Skeleton
                                            active
                                            paragraph={{ rows: 0, className: '!m-0' }}
                                            loading={config.isLoading}
                                            title={{
                                                width: '100%',
                                                className:
                                                    'm-0 mt-1 !bg-gradient-to-r from-Text/colorTextLight/[.30] from-25% via-Text/colorTextLight/[.50] via-37% to-Text/colorTextLight/[.30] to-63%'
                                            }}
                                        >
                                            {config.data?.data.organization}
                                        </Skeleton>
                                    </Text>
                                </Flex>
                            )}
                        </Flex>
                    </div>
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
