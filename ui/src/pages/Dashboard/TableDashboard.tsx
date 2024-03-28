import { Card, Popover, Space, Table, Tag, Typography } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { getAllProjects } from '../../api/interfaces';
const { Text, Title } = Typography;

interface Props {
    data: getAllProjects[];
}

const TableContainer: React.FC<Props> = ({ data }) => {
    const navigate = useNavigate();
    const tableData = data.map((el) => ({
        key: el.id,
        name: [el.name, el.description],
        members: 1,
        transactions: el.total_transactions,
        cost: el.total_cost,
        tags: el.tags.map((tag) => ({
            label: tag,
            color: 'magenta'
        }))
    }));

    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            render: (text: string[]) => (
                <Space direction="vertical" size={0}>
                    <Text style={{ fontSize: '1.1em' }}>
                        <b>{text[0]}</b>
                    </Text>
                    <Text type="secondary">{text[1]}</Text>
                </Space>
            )
        },
        {
            title: 'Members',
            dataIndex: 'members',
            key: 'members'
        },
        {
            title: 'Transactions',
            dataIndex: 'transactions',
            key: 'transactions'
        },
        {
            title: 'Total cost',
            dataIndex: 'cost',
            key: 'cost',
            render: (text: number) => `$ ${text.toFixed(4)}`
        },
        {
            title: 'Tags',
            dataIndex: 'tags',
            key: 'tags',
            render: (text: Array<{ color: string; label: string }>) => {
                return (
                    <Space size={0}>
                        {text
                            .filter((_el, id) => id < 3)
                            .map((e, id) => (
                                <Tag key={id} color={e.color}>
                                    {e.label}
                                </Tag>
                            ))}
                        {text.length > 3 && (
                            <Popover
                                content={text.map((e, id) => (
                                    <Tag key={id} color={e.color}>
                                        {e.label}
                                    </Tag>
                                ))}
                                title="Tags"
                                trigger="hover"
                            >
                                <Tag style={{ cursor: 'pointer' }}>...</Tag>
                            </Popover>
                        )}
                    </Space>
                );
            }
        }
    ];
    return (
        <Table
            style={{ gridColumn: '1 / -1' }}
            dataSource={tableData}
            columns={columns}
            pagination={false}
            onRow={(row) => {
                return {
                    onClick: () => {
                        navigate(`/projects/${row.key}`);
                    }
                };
            }}
            size="small"
            summary={() => (
                <Table.Summary fixed="top">
                    <Table.Summary.Row>
                        <Table.Summary.Cell index={0} colSpan={5}>
                            <Link to={'/projects/add'}>
                                <Card
                                    hoverable
                                    styles={{ body: { height: '100%', padding: '10px 24px' } }}
                                >
                                    <Space
                                        style={{
                                            height: '100%',
                                            width: '100%',
                                            justifyContent: 'center'
                                        }}
                                    >
                                        <Title
                                            level={2}
                                            style={{ margin: 0, textAlign: 'center', opacity: 0.5 }}
                                        >
                                            Add new project +
                                        </Title>
                                    </Space>
                                </Card>
                            </Link>
                        </Table.Summary.Cell>
                    </Table.Summary.Row>
                </Table.Summary>
            )}
            sticky={{ offsetHeader: 0 }}
        />
    );
};
export default TableContainer;
