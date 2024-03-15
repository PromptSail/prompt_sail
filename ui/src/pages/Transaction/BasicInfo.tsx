import { Badge, Collapse, Descriptions, DescriptionsProps, Flex, theme } from 'antd';
import { getTransactionResponse } from '../../api/interfaces';
import { Link } from 'react-router-dom';
import { TagsContainer } from '../../helpers/dataContainer';
import Container from '../Project/Container';
import { ArrowRightOutlined, CaretRightOutlined } from '@ant-design/icons';

interface Props {
    data: getTransactionResponse;
}

const BasicInfo: React.FC<Props> = ({ data }) => {
    const { token } = theme.useToken();
    const toLocalDate = (date: string) => {
        const local = new Date(date + 'Z');
        return `${local.toLocaleDateString()} ${local.toLocaleTimeString()}`;
    };
    const descItems: DescriptionsProps['items'] = [
        {
            label: 'Project',
            children: <Link to={`/projects/${data.project_id}`}>{data.project_name}</Link>
        },
        {
            label: 'Model',
            children: data.model
        },
        {
            label: 'Cost',
            children: '$ 1.00'
        },
        {
            label: 'Api base',
            children: data.request.url,
            span: 3
        },
        {
            label: 'Response status',
            children: <Badge status="success" text={data.status_code} />
        },
        {
            label: 'Request time',
            children: toLocalDate(data.request_time)
        },
        {
            label: 'Response time',
            children: toLocalDate(data.response_time)
        },
        {
            label: 'Tokens',
            children: (
                <span>
                    {data.response.content.usage.completion_tokens} <ArrowRightOutlined />{' '}
                    {data.response.content.usage.prompt_tokens} (Σ{' '}
                    {data.response.content.usage.total_tokens})
                </span>
            )
        },
        {
            label: 'Tags',
            children: <TagsContainer tags={data.tags} />
        },
        {
            label: 'Created by',
            children: (
                <>
                    [
                    {data.request.content.messages?.map((el, id) => (
                        <span key={id}>{id > 0 ? `, ${el.role}` : `${el.role}`}</span>
                    ))}
                    ]
                </>
            )
        }
    ];

    const collapseItems = [
        {
            key: '1',
            label: data.prompt,
            children: <p>{data.message}</p>,
            style: {
                background: token.colorFillAlter,
                borderRadius: token.borderRadiusLG,
                border: 'none'
            }
        }
    ];
    return (
        <Flex vertical gap={20}>
            <Container header={''}>
                <Descriptions items={descItems} />
            </Container>
            <Container header={'Messages'}>
                <Collapse
                    defaultActiveKey={['1']}
                    expandIcon={({ isActive }) => <CaretRightOutlined rotate={isActive ? 90 : 0} />}
                    items={collapseItems}
                />
            </Container>
        </Flex>
    );
};
export default BasicInfo;
