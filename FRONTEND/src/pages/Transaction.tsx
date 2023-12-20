import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useEffect } from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { useGetTransaction } from '../api/queries';

const Transaction: React.FC = () => {
    const params = useParams();
    const navigate = useNavigate();
    const transaction = useGetTransaction(params.transactionId || '');
    const { project } = useLocation().state || { project: null };
    useEffect(() => {
        if (project === null && transaction.isSuccess) {
            navigate(`/projects/${transaction.data.data.project_id}`, {
                state: params.transactionId
            });
        }
    }, [transaction.isSuccess]);
    if (transaction)
        if (transaction.isLoading)
            return (
                <>
                    <div>loading...</div>
                </>
            );
    if (transaction.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transaction.error)}
                {navigate('/')}
            </>
        );
    if (transaction.isSuccess && project !== null) {
        const data = transaction.data.data;
        return (
            <>
                <div className="p-5 px-20 pt-[100px]">
                    <h1 className="text-4xl font-semibold">
                        Transaction details - {data.id} in {project.name}
                    </h1>
                    <div className="border-4">
                        <div className="border-b-4 p-3 flex flex-row gap-16">
                            <span>Model {data.request.content.model}</span>
                            <span>Cost $ 0.05</span>
                            <span>
                                Rate: [{data.response.content.usage.prompt_tokens}+] [
                                {data.response.content.usage.completion_tokens}]
                            </span>
                        </div>
                        <div className="border-b-4 p-3 flex flex-row gap-16">
                            <span>{data.request.url}</span>
                            <span>Response status: {data.response.status_code}</span>
                        </div>
                        <div className="border-b-4 p-3 flex flex-row gap-16">
                            <span>Timestamp: {data.timestamp}</span>
                            <span>
                                Created by{' '}
                                {data.request.content.messages?.map((el, id) => (
                                    <span key={id}>{id > 0 ? `, ${el.role}` : `${el.role}`}</span>
                                ))}
                            </span>
                            <span>Tags: </span>
                        </div>
                        <div className="border-b-4 w-full flex flex-row">
                            <div className="border-e-4 p-2">Input</div>
                            <div className="p-2">
                                {data.request.content.messages?.map((el, id) => (
                                    <span key={id}>[{el.content}]</span>
                                ))}
                            </div>
                        </div>
                        <div className="w-full flex flex-row">
                            <div className="p-2 m-auto">Output</div>
                            <div className="border-s-4 p-2">
                                {data.response.content.choices.map((el, id) => (
                                    <span key={id}>[{el.message.content}]</span>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
                <div className="my-5">
                    <SyntaxHighlighter
                        language="python"
                        style={styles.atomOneDark}
                        customStyle={{ display: 'inline' }}
                    >{`http://${project.id}.promptsail.local`}</SyntaxHighlighter>
                    <span className="hidden md:inline">&rArr;</span>
                    <span className="block md:hidden my-5 ms-3">&dArr;</span>
                    <SyntaxHighlighter
                        language="python"
                        style={styles.atomOneDark}
                        customStyle={{ display: 'inline' }}
                    >
                        {project.api_base}
                    </SyntaxHighlighter>
                </div>
                <h2 className="text-2xl font-semibold">Request</h2>
                <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                    {JSON.stringify(data.request, null, 4)}
                </SyntaxHighlighter>
                <h3 className="text-2xl font-semibold">Response</h3>
                <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                    {JSON.stringify(data.response, null, 4)}
                </SyntaxHighlighter>
                <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                    {`timestamp: ${JSON.stringify(data.timestamp, null, 4)},
status_code: ${JSON.stringify(data.response.status_code, null, 4)},
processing_time: ${JSON.stringify(data.response.elapsed, null, 4)}
                `}
                </SyntaxHighlighter>
            </>
        );
    }
};

export default Transaction;
