import { Link, useNavigate } from 'react-router-dom';
import { useGetProject } from '../../api/queries';
import { getTransactionResponse } from '../../api/interfaces';
import SyntaxHighlighter from 'react-syntax-highlighter';
import * as styles from 'react-syntax-highlighter/dist/esm/styles/hljs';

interface Params {
    transaction: getTransactionResponse;
}

const TransactionAndProjectDetails: React.FC<Params> = ({ transaction }) => {
    const navigate = useNavigate();
    const project = useGetProject(transaction.project_id);
    const toLocalDate = (date: string) => {
        const local = new Date(date + 'Z');
        return `${local.toLocaleDateString()} ${local.toLocaleTimeString()}`;
    };
    if (project.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (project.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(project.error)}
                {navigate('/')}
            </>
        );
    if (project.isSuccess) {
        const projectData = project.data.data;
        return (
            <>
                <div className="p-5 px-20 pt-[100px]">
                    <h1 className="text-4xl font-semibold">
                        Transaction details - {transaction.id} in{' '}
                        <Link className="underline" to={`/projects/${projectData.id}`}>
                            {projectData.name}
                        </Link>
                    </h1>
                    <div className="border-4">
                        <div className="border-b-4 p-3 flex flex-row gap-16">
                            <span>Model {transaction.request.content.model}</span>
                            <span>Cost $ 0.05</span>
                            <span>
                                Rate: [{transaction.response.content.usage.prompt_tokens}+] [
                                {transaction.response.content.usage.completion_tokens}]
                            </span>
                        </div>
                        <div className="border-b-4 p-3 flex flex-row gap-16">
                            <span>{transaction.request.url}</span>
                            <span>Response status: {transaction.response.status_code}</span>
                        </div>
                        <div className="border-b-4 p-3 flex flex-row gap-16">
                            <span>request_time: {toLocalDate(transaction.request_time)}</span>
                            <span>response_time: {toLocalDate(transaction.response_time)}</span>
                            <span>
                                Created by{' {'}
                                {transaction.request.content.messages?.map((el, id) => (
                                    <span key={id}>[{id > 0 ? `, ${el.role}` : `${el.role}`}]</span>
                                ))}
                                {'}'}
                            </span>
                            <span>Tags: {`${transaction.tags}`}</span>
                        </div>
                        <div className="border-b-4 w-full flex flex-row">
                            <div className="border-e-4 p-2">Input</div>
                            <div className="p-2">{transaction.prompt}</div>
                        </div>
                        <div className="w-full flex flex-row">
                            <div className="p-2 m-auto">Output</div>
                            <div className="border-s-4 p-2">{transaction.message}</div>
                        </div>
                    </div>
                </div>
                <div>
                    {/* <div className="my-5">
                        <SyntaxHighlighter
                            language="python"
                            style={styles.atomOneDark}
                            customStyle={{ display: 'inline' }}
                        >{`http://localhost:8000/${projectData.slug}/${transaction.}`}</SyntaxHighlighter>
                        <span className="hidden md:inline">&rArr;</span>
                        <span className="block md:hidden my-5 ms-3">&dArr;</span>
                        <SyntaxHighlighter
                            language="python"
                            style={styles.atomOneDark}
                            customStyle={{ display: 'inline' }}
                        >
                            {projectData.ai_providers[0].api_base}
                        </SyntaxHighlighter>
                    </div> */}
                    <h2 className="text-2xl font-semibold">Request</h2>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {JSON.stringify(transaction.request, null, 4)}
                    </SyntaxHighlighter>
                    <h3 className="text-2xl font-semibold">Response</h3>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {JSON.stringify(transaction.response, null, 4)}
                    </SyntaxHighlighter>
                    <SyntaxHighlighter language="python" style={styles.atomOneDark}>
                        {`request_time: ${JSON.stringify(transaction.request_time, null, 4)},
response_time: ${JSON.stringify(transaction.response_time, null, 4)},
status_code: ${JSON.stringify(transaction.response.status_code, null, 4)},
processing_time: ${JSON.stringify(transaction.response.elapsed, null, 4)}
                        `}
                    </SyntaxHighlighter>
                </div>
            </>
        );
    }
};

export default TransactionAndProjectDetails;
