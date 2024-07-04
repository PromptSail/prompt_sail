import { Flex, Select, SelectProps, Typography } from 'antd';
import { useGetUsers } from '../../api/queries';
import { useEffect, useState } from 'react';
import DefaultAvatar from '../../components/DefaultAvatar/DefaultAvatar';
const { Text } = Typography;
interface Props extends SelectProps {}
const UserFilter: React.FC<Props> = ({ ...rest }) => {
    const [options, setOptions] = useState<{ label: JSX.Element | string; value: string }[]>([]);
    const users = useGetUsers();
    useEffect(() => {
        if (users.isSuccess) {
            setOptions(
                users.data?.data.map((user) => ({
                    label: <UserComponent img={user.picture} label={user.email} />,
                    value: user.email
                }))
            );
        }
    }, [users.status]);
    return (
        <Select
            {...rest}
            options={options}
            loading={users.isLoading}
            placeholder="Select"
            allowClear
        />
    );
};
const UserComponent: React.FC<{ img: string | null; label: string }> = ({ img, label }) => {
    return (
        <Flex gap={8}>
            {img !== null && img.length > 0 ? (
                <img
                    referrerPolicy="no-referrer"
                    src={img}
                    alt={`avatar_${label}`}
                    className="w-[24px] h-[24px] rounded-full"
                />
            ) : (
                <DefaultAvatar circle={24} icon={14} />
            )}

            <Text className="my-auto">{label}</Text>
        </Flex>
    );
};

export default UserFilter;
