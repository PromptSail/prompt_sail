import { Flex, Select, SelectProps, Typography } from 'antd';
import { useContext, useEffect, useState } from 'react';
import { Context } from '../../context/Context';
import api from '../../api/api';
import { useFormikContext } from 'formik';
import { FormikValuesTemplate } from './types';
import defAvatar from '../../assets/logo/symbol-white.svg';
const { Text } = Typography;

interface Props extends SelectProps {}

const UserSelect: React.FC<Props> = ({ ...rest }) => {
    const config = useContext(Context).config;
    const [options, setOptions] = useState<{ label: JSX.Element | string; value: string }[]>([]);
    const { setFieldValue, values, handleChange } = useFormikContext<typeof FormikValuesTemplate>();
    useEffect(() => {
        if (config !== null) {
            if (config.authorization) {
                api.getUsers().then((data) => {
                    setOptions(
                        data.data.map((user, id) => ({
                            label: <UserComponent img={user.picture} label={user.email} />,
                            value: user.email + id
                        }))
                    );
                    setFieldValue('owner', data.data[0].email + 0);
                });
            } else {
                api.whoami().then((data) => {
                    setOptions(() => [
                        {
                            label: (
                                <UserComponent img={data.data.picture} label={data.data.email} />
                            ),
                            value: data.data.email
                        }
                    ]);
                    setFieldValue('owner', data.data.email);
                });
            }
        }
    }, [config]);
    return (
        <Select
            {...rest}
            value={values.owner}
            onChange={(val) => {
                handleChange({
                    target: {
                        value: val,
                        name: 'owner'
                    }
                });
            }}
            size="large"
            options={options}
            loading={config === null || options.length == 0}
            disabled={true && !config?.authorization}
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
                    className="w-[32px] h-[32px] rounded-full"
                />
            ) : (
                // <iframe src={img} />
                <div className="w-[32px] h-[32px] bg-Primary/colorPrimary rounded-full relative my-auto">
                    <img
                        src={defAvatar}
                        alt={`avatar_${label}`}
                        className="w-[21px] h-[21px] absolute top-[14%] left-[13%]"
                    />
                </div>
            )}

            <Text className="my-auto">{label}</Text>
        </Flex>
    );
};

export default UserSelect;
