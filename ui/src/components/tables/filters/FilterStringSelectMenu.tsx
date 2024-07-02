import { FilterDropdownProps } from 'antd/es/table/interface';
import { TransactionsFilters } from '../../../api/types';
import { Key, SetStateAction, useEffect, useState } from 'react';
import { UseQueryResult } from 'react-query';
import { AxiosError } from 'axios';
import { Button, Divider, Flex, Input, Menu, Skeleton, Tree } from 'antd';
import { DefaultOptionType } from 'antd/es/select';

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
    return (
        <Flex vertical>
            <Input
                className="m-[4px] w-[calc(100%-8px)]"
                placeholder="Search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <div className="max-h-[150px] overflow-y-auto overflow-x-hidden">
                {strings.isLoading ? (
                    <div className="relative h-[150px]">
                        <Skeleton
                            className="w-full"
                            active
                            title={false}
                            paragraph={{
                                rows: 10,
                                style: {
                                    margin: '15px'
                                }
                            }}
                        />
                    </div>
                ) : target === 'provider_models' ? (
                    <Tree
                        checkable
                        className="m-1"
                        defaultExpandAll
                        onCheck={(k) => {
                            const keys = k as Key[];
                            const parents = keys.filter((key) => !(key as string).includes('.'));
                            const normalizedKeys = [
                                ...keys.filter(
                                    (key) =>
                                        !parents.some((parent) =>
                                            !search.length
                                                ? (key as string).split('.')[0] === parent
                                                : (key as string) === parent
                                        )
                                )
                            ];
                            if (!search.length) normalizedKeys.push(...parents);
                            setSelectedKeys(normalizedKeys);
                        }}
                        checkedKeys={selectedKeys}
                        treeData={(() => {
                            const grouped: { [key: string]: string[] } = {};
                            strings.data?.map((el) => {
                                const model = el['model_name'];
                                const provider = el['provider'];
                                if (!grouped[provider]) grouped[provider] = [];
                                grouped[provider].push(model);
                            });
                            const items: DefaultOptionType[] = Object.keys(grouped).map(
                                (provider) => ({
                                    key: provider,
                                    title: provider,
                                    children: grouped[provider].map((model: string) => ({
                                        key: provider + '.' + model,
                                        title: model
                                    }))
                                })
                            );
                            // console.log(items);
                            return items;
                        })()
                            .filter(
                                (el) =>
                                    el.title?.toLowerCase().includes(search) ||
                                    el.children?.some((child) =>
                                        child.title?.toLowerCase().includes(search)
                                    )
                            )
                            .map((el) => ({
                                ...el,
                                children: el.children?.filter((child) =>
                                    child.title?.toLowerCase().includes(search)
                                )
                            }))}
                    />
                ) : (
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
                )}
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
                    Search
                </Button>
            </Flex>
        </Flex>
    );
};
export default FilterStringSelectMenu;
