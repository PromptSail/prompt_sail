import {
    CheckOutlined,
    RedoOutlined,
    SearchOutlined,
    SortAscendingOutlined,
    SortDescendingOutlined
} from '@ant-design/icons';
import { Button, Flex, Form, Input, Select, theme } from 'antd';
import React from 'react';
import { useState } from 'react';
import SelectForm from './SelectForm';
const { useToken } = theme;
const FilterDashboard: React.FC = () => {
    const { token } = useToken();
    const [isAsc, setAsc] = useState(true);
    const [costRange, setCostRnage] = useState({ start: 0, end: 100 });
    const [transactionsRange, setTransactionsRange] = useState({ start: 0, end: 100 });
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
                            suffix={<SearchOutlined />}
                        />
                    </Form.Item>
                    <Form.Item className="m-0 max-w-[295px] w-full" label="Sort by" name="sort">
                        <div className="flex gap-[4px]">
                            <Select
                                className="max-w-[200px]"
                                defaultValue={'title'}
                                menuItemSelectedIcon={<CheckOutlined />}
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
                                onClick={() => setAsc(!isAsc)}
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
                    <Form.Item className="m-0 max-w-[253px] w-full" label="Owner" name="owner">
                        <Select
                            placeholder="Select"
                            options={[
                                { value: 'owner1', label: 'owner1' },
                                { value: 'owner2', label: 'owner2' },
                                { value: 'owner3', label: 'owner3' }
                            ]}
                        />
                    </Form.Item>
                    <Form.Item className="m-0 max-w-[241px] w-full" label="Cost" name="cost">
                        <SelectForm values={costRange} onChange={setCostRnage} prefix="$ " />
                    </Form.Item>
                    <Form.Item
                        className="m-0 max-w-[292px] w-full"
                        label="Transactions"
                        name="transactions"
                    >
                        <SelectForm values={transactionsRange} onChange={setTransactionsRange} />
                    </Form.Item>
                    {!isAsc && (
                        <Button
                            type="text"
                            className={`text-[${token.colorPrimary}]`}
                            icon={<RedoOutlined />}
                            onClick={() => {
                                console.log('clear');
                                setAsc(!isAsc);
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
