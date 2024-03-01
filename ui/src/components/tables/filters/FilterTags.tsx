import { SetStateAction } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { Select, Tag } from 'antd';

interface Props {
    defaultValue: string;
    setFilters: (args: SetStateAction<TransactionsFilters>) => void;
    setTags: (tags: string) => void;
}

const FilterTags: React.FC<Props> = ({ defaultValue, setFilters, setTags }) => {
    const options = [
        {
            label: 'tag1',
            value: 'magenta'
        },
        {
            label: 'tag2',
            value: 'red'
        },
        {
            label: 'tag3',
            value: 'volcano'
        },
        {
            label: 'tag4',
            value: 'blue'
        },
        {
            label: 'tag5',
            value: 'cyan'
        },
        {
            label: 'tag6',
            value: 'purple'
        }
    ];
    const defaults: typeof options = [];
    if (defaultValue.length > 0)
        defaultValue.split(',').map((el) => {
            console.log(el);
            defaults.push({ label: el, value: 'magenta' });
        });
    return (
        <Select
            mode="multiple"
            allowClear
            style={{ width: 250 }}
            tagRender={({ label, value, closable, onClose }) => {
                return (
                    <Tag color={value} closable={closable} onClose={onClose}>
                        {label}
                    </Tag>
                );
            }}
            placeholder="Select tags"
            defaultValue={defaults}
            options={options}
        />
    );
};
export default FilterTags;
