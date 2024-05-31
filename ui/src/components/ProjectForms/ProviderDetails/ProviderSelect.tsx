import { Select } from 'antd';
import { useGetProviders } from '../../../api/queries';
import { SizeType } from 'antd/es/config-provider/SizeContext';

interface Props {
    className?: string;
    value: string;
    size?: SizeType;
    onChange?: (
        value: string,
        option:
            | {
                  label: string;
                  value: string;
              }
            | {
                  label: string;
                  value: string;
              }[]
    ) => void;
}

const ProviderSelect: React.FC<Props> = ({ className, value, size, onChange }) => {
    const Providers = useGetProviders();
    return (
        <Select
            className={className}
            value={value}
            size={size}
            onChange={onChange}
            options={[
                { label: 'Select Provider', value: '' },
                ...(Providers.data?.data.map((el) => ({
                    label: el.provider_name,
                    value: el.provider_name
                })) || [])
            ]}
            loading={Providers.isLoading}
        />
    );
};

export default ProviderSelect;
