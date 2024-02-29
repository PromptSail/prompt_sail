import { Tag, Typography, Flex, Select, DatePicker } from 'antd';
import { useSearchParams } from 'react-router-dom';
import { TransactionsFilters } from '../api/types';
import { useEffect, useState } from 'react';
import { useGetAllTransactions } from '../api/queries';
import TransactionsTable from '../components/tables/AllTransactions/TransactionsTable';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const Transactions = () => {
    const [params, setParams] = useSearchParams();
    const [filters, setFilters] = useState<TransactionsFilters>({
        project_id: params.get('project_id') || '',
        tags: params.get('tags') || '',
        date_from: params.get('date_from') || '',
        date_to: params.get('date_to') || '',
        page_size: params.get('page_size') || '10'
    });
    const transactions = useGetAllTransactions(filters);
    const [{ page, totalPages, totalElements }, setPagesInfo] = useState({
        page: -1,
        totalPages: -1,
        totalElements: -1
    });
    useEffect(() => {
        if (transactions.isSuccess) {
            setPagesInfo({
                page: transactions.data.data.page_index,
                totalPages: transactions.data.data.total_pages,
                totalElements: transactions.data.data.total_elements
            });
        }
    }, [transactions.status]);
    const setPage = (val: number) => {
        setFilters((old) => ({
            ...old,
            page: `${val}`
        }));
    };
    const setNewParam = (param: { [key: string]: string }) => {
        const newParam = new URLSearchParams(params);
        for (const key in param) {
            if (Object.prototype.hasOwnProperty.call(param, key)) {
                param[key].length > 0 ? newParam.set(key, param[key]) : newParam.delete(key);
            }
        }
        setParams(newParam);
    };
    if (transactions.isLoading) return <div>loading...</div>;
    if (transactions.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transactions.error)}
            </>
        );
    if (transactions.isSuccess)
        return (
            <>
                <Title level={1} style={{ margin: 0, marginBottom: 20 }}>
                    Transactions
                </Title>
                <Flex vertical gap={25}>
                    <Flex gap={10}>
                        <Select
                            defaultValue=""
                            style={{ width: 150 }}
                            options={[
                                { value: '', label: 'Select project' },
                                { value: 'Project1', label: 'Project1' },
                                { value: 'Project2', label: 'Project2' },
                                { value: 'My Project', label: 'My Project' },
                                { value: 'Project asd asd', label: 'Project asd asd' }
                            ]}
                        />
                        <RangePicker showTime />
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
                            defaultValue={[]}
                            options={[
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
                            ]}
                        />
                    </Flex>
                    <TransactionsTable data={transactions.data?.data.items} />
                </Flex>
            </>
        );
};
export default Transactions;
