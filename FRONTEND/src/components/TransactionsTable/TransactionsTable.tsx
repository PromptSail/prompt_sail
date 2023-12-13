import { Link } from 'react-router-dom';
import { TransactionResponse } from '../../api/interfaces';
import {
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    useReactTable
} from '@tanstack/react-table';
import { useState } from 'react';

interface Props {
    transactions: TransactionResponse[];
    project: {
        id: string;
        name: string;
        api_base: string;
    };
}

type transaction = {
    timestamp: string;
    requestUrl: string;
    prompt: string;
    response: string;
    model: string;
    contentType: string;
    responseStatus: string;
    usage: string;
    more: JSX.Element;
};
const columnHelper = createColumnHelper<transaction>();
const columns = [
    columnHelper.accessor('timestamp', {
        header: 'timestamp',
        cell: (info) => info.getValue()
    }),
    columnHelper.accessor((row) => row.requestUrl, {
        id: 'requestUrl',
        header: () => <span>Request URL</span>,
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('prompt', {
        header: () => 'Prompt',
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('response', {
        header: () => <span>Response</span>,
        cell: (v) => v.getValue(),
        size: 200
    }),
    columnHelper.accessor('model', {
        header: 'Model',
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('contentType', {
        header: 'Content Type',
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('responseStatus', {
        header: 'Response status',
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('usage', {
        header: 'Usage',
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('more', {
        header: 'More',
        cell: (v) => v.getValue()
    })
];

const TransactionsTable: React.FC<Props> = ({ transactions, project }) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [data, setData] = useState<transaction[]>(
        transactions.map((tr) => ({
            timestamp: tr.timestamp,
            requestUrl: tr.request.url,
            prompt: (() => {
                let str = '';
                if (tr.request.content.messages)
                    tr.request.content.messages.map((m) => (str += `{${m.role}}: ${m.content}\n`));
                else tr.request.content.prompt.map((p, id) => (str += `{prompt_${id}}: ${p}\n`));
                return str;
            })(),
            response: (() => {
                let str = '';
                tr.response.content.choices.map((c) => {
                    if (c.message) str += `{${c.message.role}}: ${c.message.content}\n`;
                    else str += `{response_${c.index}}: ${c.text}\n`;
                });
                return str;
            })(),
            model: tr.response.content.model,
            contentType: tr.response.headers['content-type'],
            responseStatus: tr.response.status_code,
            usage: `${tr.response.content.usage.prompt_tokens}+\n${tr.response.content.usage.completion_tokens}`,
            more: (
                <Link
                    id={tr.id}
                    to={`/transaction/${tr.id}`}
                    state={{
                        project: {
                            id: project.id,
                            name: project.name,
                            api_base: project.api_base
                        }
                    }}
                >
                    Details
                </Link>
            )
        }))
    );
    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel()
    });
    return (
        <>
            <h4 className="text-xl font-semibold mb-2 mt-3 md:text-2xl">LLM Transactions</h4>
            <div className="overflow-x-auto p-3">
                <table className="border-2 border-black">
                    <thead className="bg-blue-500 text-white">
                        {table.getHeaderGroups().map((hGroup) => (
                            <tr className="border-2 border-black" key={hGroup.id}>
                                {hGroup.headers.map((h) => (
                                    <th className="border-2 border-black" key={h.id}>
                                        {h.isPlaceholder
                                            ? null
                                            : flexRender(h.column.columnDef.header, h.getContext())}
                                    </th>
                                ))}
                            </tr>
                        ))}
                    </thead>

                    <tbody>
                        {table.getRowModel().rows.map((row) => (
                            <tr key={row.id}>
                                {row.getVisibleCells().map((cell) => (
                                    <td className="border-2 border-black" key={cell.id}>
                                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    );
};
export default TransactionsTable;
