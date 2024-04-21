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
            value: 'tag1'
        },
        {
            value: 'tag2'
        },
        {
            value: 'tag3'
        },
        {
            value: 'tag4'
        },
        {
            value: 'tag5'
        },
        {
            value: 'tag6'
        }
    ];
    const defaults: typeof options = [];
    if (defaultValue.length > 0)
        defaultValue.split(',').map((el) => {
            defaults.push({ value: el });
        });
    return (
        <Select
            mode="tags"
            allowClear
            style={{ width: 250 }}
            tagRender={({ value, closable, onClose }) => {
                return (
                    <Tag color="blue" closable={closable} onClose={onClose}>
                        {value}
                    </Tag>
                );
            }}
            onChange={(e) => {
                const tags = e.join(',');
                setFilters((old) => ({ ...old, tags }));
                setTags(tags);
            }}
            placeholder="Select tags"
            defaultValue={defaults}
            options={options}
        />
    );
};
export default FilterTags;
