import SyntaxHighlighter from 'react-syntax-highlighter';
import { getTransactionResponse } from '../../api/interfaces';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { Collapse, CollapseProps, Typography, theme } from 'antd';
import Container from '../../components/Container/Container';

const { Title } = Typography;
interface Props {
    data: getTransactionResponse;
}
const JSONformat: React.FC<Props> = ({ data }) => {
    const { token } = theme.useToken();
    const itemStyle = {
        background: token.colorBgContainer,
        // @ts-expect-error token.Collapse.colorBorder is correctly defined in /ui/src/theme-light.tsx
        border: `1px solid ${token.Collapse.colorBorder}`,
        borderRadius: '8px'
    };
    const items: CollapseProps['items'] = [
        {
            key: 0,
            label: (
                <Title level={2} className="h5 !m-0">
                    Request
                </Title>
            ),
            style: itemStyle,
            children: (
                <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                    {JSON.stringify(data.request, null, 4)}
                </SyntaxHighlighter>
            )
        },
        {
            key: 1,
            label: (
                <Title level={2} className="h5 !m-0">
                    Response
                </Title>
            ),
            style: itemStyle,
            children: (
                <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                    {JSON.stringify(data.response, null, 4)}
                </SyntaxHighlighter>
            )
        }
    ];
    return (
        <>
            <Container>
                <div>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {`request_time: ${JSON.stringify(data.request_time, null, 4)},
response_time: ${JSON.stringify(data.response_time, null, 4)},
status_code: ${JSON.stringify(data.response.status_code, null, 4)},
processing_time: ${JSON.stringify(data.response.elapsed, null, 4)}`}
                    </SyntaxHighlighter>
                </div>
            </Container>
            <Collapse
                defaultActiveKey={[0, 1]}
                style={{
                    background: token.Layout?.bodyBg,
                    border: 'none',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 12,
                    padding: 0
                }}
                expandIconPosition="end"
                items={items}
            />
        </>
    );
};

export default JSONformat;
