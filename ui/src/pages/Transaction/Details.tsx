import SyntaxHighlighter from 'react-syntax-highlighter';
import { getTransactionResponse } from '../../api/interfaces';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';

interface Props {
    data: getTransactionResponse;
}

const Details: React.FC<Props> = ({ data }) => {
    return (
        <>
            <h2 className="text-2xl font-semibold">Request</h2>
            <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                {JSON.stringify(data.request, null, 4)}
            </SyntaxHighlighter>
            <h3 className="text-2xl font-semibold">Response</h3>
            <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                {JSON.stringify(data.response, null, 4)}
            </SyntaxHighlighter>
            <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                {`request_time: ${JSON.stringify(data.request_time, null, 4)},
response_time: ${JSON.stringify(data.response_time, null, 4)},
status_code: ${JSON.stringify(data.response.status_code, null, 4)},
processing_time: ${JSON.stringify(data.response.elapsed, null, 4)}
                        `}
            </SyntaxHighlighter>
        </>
    );
};

export default Details;
