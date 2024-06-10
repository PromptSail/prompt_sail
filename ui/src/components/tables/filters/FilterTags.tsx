import { SetStateAction, useEffect } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { Button, Divider, Flex, Select, Tag } from 'antd';
import { FilterDropdownProps } from 'antd/es/table/interface';

interface Props {
    filters: TransactionsFilters;
    setFilters: (args: SetStateAction<TransactionsFilters>) => void;
}

const FilterTags: React.FC<FilterDropdownProps & Props> = ({
    setSelectedKeys,
    selectedKeys,
    confirm,
    setFilters,
    filters
}) => {
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
    useEffect(() => {
        if (filters.tags) setSelectedKeys(filters.tags.split(','));
    }, [filters.tags]);
    return (
        <Flex vertical>
            <Select
                mode="tags"
                className="m-1"
                allowClear
                style={{ width: 250 }}
                tagRender={({ value, closable, onClose }) => {
                    return (
                        <Tag color="blue" closable={closable} onClose={onClose}>
                            {value}
                        </Tag>
                    );
                }}
                onChange={setSelectedKeys}
                placeholder="Select tags"
                defaultValue={filters.tags ? filters.tags.split(',') : []}
                value={selectedKeys}
                options={options}
                placement="topLeft"
            />
            <Divider className="my-1" />
            <Flex justify="space-between" className="my-2 mx-2">
                <Button
                    type="text"
                    size="small"
                    onClick={() => setSelectedKeys([])}
                    disabled={!selectedKeys.length}
                >
                    Reset
                </Button>
                <Button
                    type="primary"
                    size="small"
                    onClick={() => {
                        setFilters((prevFilters) => ({
                            ...prevFilters,
                            tags: selectedKeys.join(',')
                        }));
                        confirm();
                    }}
                >
                    Save
                </Button>
            </Flex>
        </Flex>
    );
};
export default FilterTags;
