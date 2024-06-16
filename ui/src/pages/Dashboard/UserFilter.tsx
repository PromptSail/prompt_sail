import { Flex, Select, SelectProps, Typography } from 'antd';
import defAvatar from '../../assets/logo/symbol-white.svg';
import { useGetUsers } from '../../api/queries';
import { useEffect, useState } from 'react';
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
        <Flex gap={8} className="overflow-hidden max-w-[200px]">
            {img !== null && img.length > 0 ? (
                <img
                    referrerPolicy="no-referrer"
                    src={img}
                    alt={`avatar_${label}`}
                    className="w-[24px] h-[24px] rounded-full"
                />
            ) : (
                <div>
                    <div className="!w-[24px] h-[24px] bg-Primary/colorPrimary rounded-full relative my-auto">
                        <img
                            src={defAvatar}
                            alt={`avatar_${label}`}
                            className="w-[16px] h-[16px] absolute top-[15%] left-[13%]"
                        />
                    </div>
                </div>
            )}

            <Text className="my-auto">{label}</Text>
        </Flex>
    );
};

export default UserFilter;
