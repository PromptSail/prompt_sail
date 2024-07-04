import {
    CheckOutlined,
    RedoOutlined,
    SearchOutlined,
    SortAscendingOutlined,
    SortDescendingOutlined
} from '@ant-design/icons';
import { Button, Flex, Form, Input, Select } from 'antd';
import React, { useContext, useEffect } from 'react';
import { useState } from 'react';
import SelectForm from './SelectForm';
import UserFilter from './UserFilter';
import { Context } from '../../context/Context';

interface Props {
    onSearch: (text: string) => void;
    onSortAsc: (isAsc: boolean) => void;
    onSortByChange: (sortby: string) => void;
    onSetOwner: (value: string | null) => void;
    owner: string | null;
    costRange: { start: number | null; end: number | null; min?: number; max?: number };
    transactionsRange: { start: number | null; end: number | null; min?: number; max?: number };
    onChangeCost: (obj: { start: number | null; end: number | null }) => void;
    onChangeTransactions: (obj: { start: number | null; end: number | null }) => void;
}

const FilterDashboard: React.FC<Props> = ({
    onSearch,
    onSortAsc,
    onSortByChange,
    owner,
    costRange,
    transactionsRange,
    onChangeCost,
    onChangeTransactions,
    onSetOwner
}) => {
    const [isAsc, setAsc] = useState(false);
    const [isClearActive, setClear] = useState(false);
    const auth = useContext(Context).config?.authorization;
    useEffect(() => {
        if (
            (costRange.start != null && costRange.start != costRange.min) ||
            (costRange.end != null && costRange.end != costRange.max) ||
            (transactionsRange.start != null && transactionsRange.start != transactionsRange.min) ||
            (transactionsRange.end != null && transactionsRange.end != transactionsRange.max) ||
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
                    {auth && (
                        <div className="flex gap-2 m-0 max-w-[300px] w-full">
                            <label className="my-auto text-nowrap">Owner :</label>
                            <UserFilter onChange={onSetOwner} value={owner} className="w-full" />
                        </div>
                    )}
                    <Form.Item className="m-0 max-w-[241px] w-full" label="Cost" name="cost">
                        <SelectForm
                            values={costRange}
                            onChange={onChangeCost}
                            prefix="$ "
                            max={Number((costRange.max || 0).toFixed(4))}
                            fixed={4}
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
                                onChangeCost({
                                    start: costRange.min || 0,
                                    end: costRange.max || 0
                                });
                                onChangeTransactions({
                                    start: transactionsRange.min || 0,
                                    end: transactionsRange.max || 0
                                });
                                onSetOwner(null);
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
