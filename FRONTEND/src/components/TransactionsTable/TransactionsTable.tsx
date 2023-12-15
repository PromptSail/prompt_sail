import { Link } from 'react-router-dom';
import { TransactionResponse } from '../../api/interfaces';
import {
    SortingState,
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable
} from '@tanstack/react-table';
import { useState } from 'react';
import { randomTransactionData } from '../../api/test/randomTransactionsData';
import { Button, Form } from 'react-bootstrap';

declare global {
    interface Window {
        test(length: number): void;
    }
}

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
    prompt: string;
    response: string;
    model: string;
    usage: string;
    more: JSX.Element;
};
const columnHelper = createColumnHelper<transaction>();
const columns = [
    columnHelper.accessor('timestamp', {
        header: 'timestamp',
        cell: (v) => v.getValue(),
        sortingFn: 'datetime',
        size: 100
    }),
    columnHelper.accessor('prompt', {
        header: () => 'Prompt',
        cell: (v) => v.getValue(),
        size: 200
    }),
    columnHelper.accessor('response', {
        header: () => <span>Response</span>,
        cell: (v) => v.getValue(),
        size: 400
    }),
    columnHelper.accessor('model', {
        header: 'Model',
        cell: (v) => v.getValue()
    }),
    columnHelper.accessor('usage', {
        header: 'Usage',
        cell: (v) => v.getValue(),
        size: 50
    }),
    columnHelper.accessor('more', {
        header: 'More',
        cell: (v) => v.getValue(),
        size: 50,
        enableSorting: false,
        enableGlobalFilter: false
    })
];
const TransactionsTable: React.FC<Props> = ({ transactions, project }) => {
    window.test = (length: number) => {
        setData(randomTransactionData(length || 5));
    };
    const [search, setSearch] = useState('');
    const [sorting, setSorting] = useState<SortingState>([]);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [data, setData] = useState<transaction[]>(
        transactions.map((tr) => ({
            timestamp: (() => {
                const d = new Date(tr.timestamp);
                return `${d.toLocaleDateString()}\n${d.getHours()}:${d.getMinutes()}`;
            })(),
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
            model: (() => {
                return `${tr.response.content.model}\n(${tr.request.url})`;
            })(),
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
        state: { sorting, globalFilter: search },
        onSortingChange: setSorting,
        onGlobalFilterChange: setSearch,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        getPaginationRowModel: getPaginationRowModel()
    });
    return (
        <>
            <Form.Control
                value={search ?? ''}
                onChange={(obj) => {
                    console.log(obj.target.value);
                    setSearch(obj.target.value);
                }}
                placeholder="Search all columns"
            />
            <Button onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
                Prev page
            </Button>
            <Button onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
                Next page
            </Button>
            <span>
                {table.getState().pagination.pageIndex + 1} / {table.getPageCount()}
            </span>
            <h4 className="text-xl font-semibold mb-2 mt-3 md:text-2xl">LLM Transactions</h4>
            <div className="overflow-x-auto p-3">
                <table className="border-2 border-black">
                    <thead className="bg-blue-500 text-white">
                        {table.getHeaderGroups().map((hGroup) => (
                            <tr className="border-2 border-black" key={hGroup.id}>
                                {hGroup.headers.map((h) => (
                                    <th
                                        className="border-2 border-black"
                                        key={h.id}
                                        style={{ width: `${h.getSize()}px` }}
                                        onClick={h.column.getToggleSortingHandler()}
                                    >
                                        {h.isPlaceholder
                                            ? null
                                            : flexRender(h.column.columnDef.header, h.getContext())}
                                        {{ asc: ' ^', desc: ' v' }[
                                            h.column.getIsSorted() as string
                                        ] ?? null}
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
