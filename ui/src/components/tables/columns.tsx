import { ArrowRightOutlined } from '@ant-design/icons';
import { Badge, Button, Divider, Flex, Menu, Tooltip } from 'antd';
import { ColumnProps } from 'antd/es/table';
import { TransactionsFilters } from '../../api/types';
import { useGetAllProjects, useGetModels, useGetProviders } from '../../api/queries';
import { ColumnFilterItem } from 'antd/es/table/interface';
import { SetStateAction } from 'react';
import FilterStringSelectMenu from './filters/FilterStringSelectMenu';
import FilterTags from './filters/FilterTags';

export interface DataType {
    key: React.Key;
    id: React.ReactNode;
    time: string;
    speed: string;
    messages: React.ReactNode;
    status: React.ReactNode;
    project: React.ReactNode;
    aiProvider: string;
    model: string;
    tags: React.ReactNode;
    cost: string;
    tokens: React.ReactNode;
}

// eslint-disable-next-line react-refresh/only-export-components
const Status: React.FC<{ value: number }> = ({ value }) => (
    <Badge status={value >= 300 ? (value >= 400 ? 'error' : 'warning') : 'success'} text={value} />
);
export type CustomColumns = ColumnProps<DataType> & {
    apiCol?: TransactionsFilters['sort_field'];
};

const columns = (
    filters: TransactionsFilters,
    setFilters: (attr: SetStateAction<TransactionsFilters>) => void
): CustomColumns[] => {
    return [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            width: 150
        },
        {
            title: 'Time',
            dataIndex: 'time',
            key: 'time',
            sorter: true,
            apiCol: 'request_time',
            width: 160
        },
        {
            title: (
                <Tooltip placement="top" title="Tokens per second">
                    Speed
                </Tooltip>
            ),
            dataIndex: 'speed',
            key: 'speed',
            sorter: true,
            apiCol: 'generation_speed',
            width: 120
        },
        {
            title: 'Messages',
            dataIndex: 'messages',
            key: 'messages',
            width: 280
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            sorter: true,
            apiCol: 'status_code',
            width: 120,
            filters: [200, 300, 400, 500].map((el) => ({
                text: <Status value={el} />,
                value: el
            })),
            filterDropdown: ({ setSelectedKeys, selectedKeys, confirm }) => {
                const items = [200, 300, 400, 500].map((el) => ({
                    label: <Status value={el} />,
                    key: el
                }));
                return (
                    <Flex vertical>
                        <Menu
                            items={items}
                            selectable
                            multiple
                            onSelect={(val) => {
                                setSelectedKeys(val.selectedKeys);
                            }}
                            onDeselect={(val) => {
                                setSelectedKeys(val.selectedKeys);
                            }}
                            defaultSelectedKeys={
                                filters.status_codes
                                    ? [...filters.status_codes.split(',')]
                                    : (selectedKeys as string[])
                            }
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
                                        status_codes: `${selectedKeys}`
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
        },
        {
            title: 'Project',
            dataIndex: 'project',
            key: 'project',
            width: 200,
            filterDropdown: (props) => (
                <FilterStringSelectMenu
                    {...props}
                    filters={filters as ColumnFilterItem[] & TransactionsFilters}
                    setFilters={setFilters}
                    query={{ hook: useGetAllProjects, label: 'name' }}
                    target="project_id"
                    multiselect={false}
                />
            )
        },
        {
            title: 'AI provider',
            dataIndex: 'aiProvider',
            key: 'aiProvider',
            sorter: true,
            apiCol: 'provider',
            width: 200,
            filterDropdown: (props) => (
                <FilterStringSelectMenu
                    {...props}
                    filters={filters as ColumnFilterItem[] & TransactionsFilters}
                    setFilters={setFilters}
                    query={{ hook: useGetProviders, label: 'provider_name' }}
                    target="providers"
                    multiselect={true}
                />
            )
        },
        {
            title: 'Model',
            dataIndex: 'model',
            key: 'model',
            sorter: true,
            apiCol: 'model',
            width: 220,
            filterDropdown: (props) => (
                <FilterStringSelectMenu
                    {...props}
                    filters={filters as ColumnFilterItem[] & TransactionsFilters}
                    setFilters={setFilters}
                    query={{ hook: useGetModels, label: 'model_name' }}
                    target="models"
                    multiselect={true}
                />
            )
        },
        {
            title: 'Tags',
            dataIndex: 'tags',
            key: 'tags',
            sorter: true,
            apiCol: 'tags',
            width: 220,
            filterDropdown: (props) => (
                <FilterTags
                    {...props}
                    filters={filters as ColumnFilterItem[] & TransactionsFilters}
                    setFilters={setFilters}
                />
            )
        },
        {
            title: 'Cost',
            dataIndex: 'cost',
            key: 'cost',
            width: 200
        },
        {
            title: (
                <Tooltip
                    placement="top"
                    title={
                        <span>
                            input <ArrowRightOutlined /> output (Σ total)
                        </span>
                    }
                >
                    Tokens
                </Tooltip>
            ),
            dataIndex: 'tokens',
            key: 'tokens',
            width: 170
        }
    ];
};
export default columns;
