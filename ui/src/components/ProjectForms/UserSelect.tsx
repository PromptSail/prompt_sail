import { Flex, Select, SelectProps, Typography } from 'antd';
import { useContext, useEffect, useState } from 'react';
import { Context } from '../../context/Context';
import api from '../../api/api';
import { useFormikContext } from 'formik';
import { FormikValuesTemplate } from './types';
import DefaultAvatar from '../DefaultAvatar/DefaultAvatar';
const { Text } = Typography;

interface Props extends SelectProps {}

const UserSelect: React.FC<Props> = ({ ...rest }) => {
    const config = useContext(Context).config;
    const [options, setOptions] = useState<{ label: JSX.Element | string; value: string }[]>([]);
    const { setFieldValue, values, handleChange } = useFormikContext<typeof FormikValuesTemplate>();
    useEffect(() => {
        if (config !== null) {
            if (config.authorization) {
                if (values.owner !== '__UPDATE__')
                    api.getUsers().then((data) => {
                        setOptions(() => {
                            const list = data.data.map((user) => ({
                                label: <UserComponent img={user.picture} label={user.email} />,
                                value: user.email
                            }));
                            if (values.owner.length > 0) {
                                if (list.map((item) => item.value).includes(values.owner)) {
                                    const owner = list.filter(
                                        (item) => item.value === values.owner
                                    )[0];
                                    const rest = list.filter((item) => item.value !== owner.value);
                                    list.splice(0, list.length);
                                    list.push(owner, ...rest);
                                } else
                                    list.unshift({
                                        label: <UserComponent img={''} label={values.owner} />,
                                        value: values.owner
                                    });
                            }
                            return list;
                        });
                        setFieldValue(
                            'owner',
                            !values.owner.length ? data.data[0].email : values.owner
                        );
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
    }, [config, values]);
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
                <DefaultAvatar />
            )}

            <Text className="my-auto">{label}</Text>
        </Flex>
    );
};

export default UserSelect;
