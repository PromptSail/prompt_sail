import {
    CheckOutlined,
    RedoOutlined,
    SearchOutlined,
    SortAscendingOutlined,
    SortDescendingOutlined
} from '@ant-design/icons';
import { Button, Flex, Form, Input, Select } from 'antd';
import React, { useEffect } from 'react';
import { useState } from 'react';
import SelectForm from './SelectForm';

interface Props {
    onSearch: (text: string) => void;
    onSortAsc: (isAsc: boolean) => void;
    onSortByChange: (sortby: string) => void;
    onSetOwner: (value: string) => void;
    costRange: { start: number | null; end: number | null; min?: number; max?: number };
    transactionsRange: { start: number | null; end: number | null; min?: number; max?: number };
    onChangeCost: (obj: { start: number | null; end: number | null }) => void;
    onChangeTransactions: (obj: { start: number | null; end: number | null }) => void;
}

const FilterDashboard: React.FC<Props> = ({
    onSearch,
    onSortAsc,
    onSortByChange,
    costRange,
    transactionsRange,
    onChangeCost,
    onChangeTransactions
}) => {
    const [isAsc, setAsc] = useState(false);
    const [owner, setOwner] = useState<string | null>(null);
    const [isClearActive, setClear] = useState(false);
    useEffect(() => {
        if (
            costRange.start != null ||
            costRange.end != null ||
            transactionsRange.start != null ||
            transactionsRange.end != null ||
            owner != null
        )
            setClear(true);
        else setClear(false);
    }, [costRange, transactionsRange, owner]);
    return (
        <Form>
            <Flex
                className="bg-white border border-solid border-[#F0F0F0] rounded-[8px] py-[15px] divide-y divide-solid divide-[#F0F0F0]"
                vertical
            >
                <Flex className="px-[24px] pb-[16px] flex-wrap" justify="space-between" gap={12}>
                    <Form.Item className="m-0 flex-auto" label="Search by keywords" name="keywords">
                        <Input
                            className="max-w-[372px] w-full"
                            placeholder="Search"
                            onChange={(e) => {
                                const val = e.currentTarget.value;
                                onSearch(val);
                            }}
                            suffix={<SearchOutlined />}
                            allowClear
                        />
                    </Form.Item>
                    <Form.Item className="m-0 max-w-[295px] w-full" label="Sort by" name="sort">
                        <div className="flex gap-[4px]">
                            <Select
                                className="max-w-[200px]"
                                defaultValue={'title'}
                                menuItemSelectedIcon={<CheckOutlined />}
                                onChange={onSortByChange}
                                options={[
                                    {
                                        value: 'title',
                                        label: 'Title'
                                    },
                                    {
                                        value: 'transactions',
                                        label: 'Transactions'
                                    },
                                    {
                                        value: 'cost',
                                        label: 'Cost'
                                    }
                                ]}
                            />
                            <Button
                                className="w-[32px]"
                                type="text"
                                onClick={() => {
                                    onSortAsc(!isAsc);
                                    setAsc(!isAsc);
                                }}
                                icon={
                                    isAsc ? (
                                        <SortAscendingOutlined className="text-[16px]" />
                                    ) : (
                                        <SortDescendingOutlined className="text-[16px]" />
                                    )
                                }
                            />
                        </div>
                    </Form.Item>
                </Flex>
                <Flex
                    className="px-[24px] pt-[16px] border-0 flex-wrap"
                    justify="flex-start"
                    gap={32}
                >
                    <div className="flex gap-2 m-0 max-w-[253px] w-full">
                        <label className="my-auto text-nowrap">Owner :</label>
                        <Select
                            placeholder="Select"
                            className="w-full"
                            options={[
                                { value: 'owner1', label: 'Owner1' },
                                { value: 'owner2', label: 'Owner2' },
                                { value: 'owner3', label: 'Owner3' }
                            ]}
                            value={owner}
                            onChange={setOwner}
                        />
                    </div>
                    <Form.Item className="m-0 max-w-[241px] w-full" label="Cost" name="cost">
                        <SelectForm
                            values={costRange}
                            onChange={onChangeCost}
                            prefix="$ "
                            max={costRange.max}
                            fixed={7}
                        />
                    </Form.Item>
                    <Form.Item
                        className="m-0 max-w-[292px] w-full"
                        label="Transactions"
                        name="transactions"
                    >
                        <SelectForm
                            values={transactionsRange}
                            onChange={onChangeTransactions}
                            max={transactionsRange.max}
                            fixed={0}
                        />
                    </Form.Item>
                    {isClearActive && (
                        <Button
                            type="text"
                            className="text-Primary/colorPrimary"
                            icon={<RedoOutlined />}
                            onClick={() => {
                                onChangeCost({ start: null, end: null });
                                onChangeTransactions({ start: null, end: null });
                                setOwner(null);
                            }}
                        >
                            Clear filters
                        </Button>
                    )}
                </Flex>
            </Flex>
        </Form>
    );
};
export default FilterDashboard;
