import { FilterDropdownProps } from 'antd/es/table/interface';
import { TransactionsFilters } from '../../../api/types';
import { SetStateAction, useEffect, useState } from 'react';
import { UseQueryResult } from 'react-query';
import { AxiosError } from 'axios';
import { Button, Divider, Flex, Input, Menu, Spin } from 'antd';

const FilterStringSelectMenu: React.FC<
    FilterDropdownProps & {
        filters: TransactionsFilters;
        setFilters: (attr: SetStateAction<TransactionsFilters>) => void;
        query: {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            hook: () => UseQueryResult<{ [key: string]: any }[], AxiosError>;
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            label: keyof { [key: string]: any };
        };
        target: keyof TransactionsFilters;
        multiselect: boolean;
    }
> = ({
    setSelectedKeys,
    selectedKeys,
    confirm,
    filters,
    setFilters,
    query,
    target,
    multiselect
}) => {
    const strings = query.hook();
    const [search, setSearch] = useState('');
    useEffect(() => {
        if (strings.isSuccess)
            setSelectedKeys(
                filters[target]
                    ? multiselect
                        ? (filters[target] as string).split(',')
                        : [filters[target] as string]
                    : []
            );
    }, [strings.status]);
    if (strings.isLoading) {
        return (
            <Spin
                size="large"
                className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/3"
            />
        );
    }
    if (!strings.isLoading) {
        return (
            <Flex vertical>
                <Input
                    className="m-1 max-w-[150px]"
                    placeholder="Search"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
                <div className="max-h-[150px] overflow-y-auto overflow-x-hidden">
                    <Menu
                        className="!max-h-full"
                        items={
                            strings.isError
                                ? [
                                      {
                                          key: strings.error.code || 'error',
                                          label: `${strings.error.message}`
                                      }
                                  ]
                                : strings.data
                                      ?.map((el) => ({
                                          key: el.id || el[query.label] || '',
                                          label: el[query.label]
                                      }))
                                      .filter(({ label }) =>
                                          search.length > 0
                                              ? label.toLowerCase().includes(search.toLowerCase())
                                              : true
                                      )
                        }
                        selectable
                        multiple={multiselect}
                        onSelect={(val) => {
                            setSelectedKeys(val.selectedKeys);
                        }}
                        onDeselect={(val) => {
                            setSelectedKeys(val.selectedKeys);
                        }}
                        selectedKeys={selectedKeys as string[]}
                    />
                </div>
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
                                [target]: `${multiselect ? selectedKeys.join(',') : selectedKeys}`
                            }));
                            confirm();
                        }}
                    >
                        Save
                    </Button>
                </Flex>
            </Flex>
        );
    }
};
export default FilterStringSelectMenu;
