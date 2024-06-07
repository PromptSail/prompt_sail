import { ArrowRightOutlined } from '@ant-design/icons';
import { Badge, Button, Divider, Flex, Input, Menu, Spin, Tooltip } from 'antd';
import { ColumnProps } from 'antd/es/table';
import { TransactionsFilters } from '../../api/types';
import { useGetAllProjects } from '../../api/queries';
import { ColumnFilterItem, FilterDropdownProps } from 'antd/es/table/interface';
import { SetStateAction, useEffect, useState } from 'react';

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

// eslint-disable-next-line react-refresh/only-export-components
const ProjectMenu: React.FC<
    FilterDropdownProps & {
        filters: TransactionsFilters;
        setFilters: (attr: SetStateAction<TransactionsFilters>) => void;
    }
> = ({ setSelectedKeys, selectedKeys, filters, setFilters, close }) => {
    const projects = useGetAllProjects();
    const [search, setSearch] = useState('');
    useEffect(() => {
        console.log(selectedKeys);
        if (projects.isSuccess) setSelectedKeys(filters.project_id ? [filters.project_id] : []);
    }, [projects.status]);
    if (projects.isLoading) {
        <Spin
            size="large"
            className="absolute top-1/3 left-1/2 -transtaction-x-1/2 -transtaction-y-1/3"
        />;
    }
    if (!projects.isLoading) {
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
                        items={
                            projects.isError
                                ? [
                                      {
                                          key: projects.error.code || 'error',
                                          label: `${projects.error.message}`
                                      }
                                  ]
                                : projects.data
                                      ?.map((el) => ({ key: el.id || '', label: el.name }))
                                      .filter(({ label }) =>
                                          search.length > 0
                                              ? label.toLowerCase().includes(search.toLowerCase())
                                              : true
                                      )
                        }
                        selectable
                        onSelect={(val) => {
                            setSelectedKeys(val.selectedKeys);
                        }}
                        defaultSelectedKeys={[filters.project_id || '']}
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
                                project_id: `${selectedKeys}`
                            }));
                            close();
                        }}
                    >
                        Save
                    </Button>
                </Flex>
            </Flex>
        );
    }
};
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
            onFilter: (value, record) => {
                const status = record.status as JSX.Element;

                return String(status.props['text']).charAt(0) == String(value).charAt(0);
            },
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
                            selectedKeys={selectedKeys as string[]}
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
                            <Button type="primary" size="small" onClick={() => confirm()}>
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
                <ProjectMenu
                    {...props}
                    filters={filters as ColumnFilterItem[] & TransactionsFilters}
                    setFilters={setFilters}
                />
            )
        },
        {
            title: 'AI provider',
            dataIndex: 'aiProvider',
            key: 'aiProvider',
            sorter: true,
            apiCol: 'provider',
            width: 200
        },
        {
            title: 'Model',
            dataIndex: 'model',
            key: 'model',
            sorter: true,
            apiCol: 'model',
            width: 220
        },
        {
            title: 'Tags',
            dataIndex: 'tags',
            key: 'tags',
            sorter: true,
            apiCol: 'tags',
            width: 220
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
