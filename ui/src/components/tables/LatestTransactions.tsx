import { Link } from 'react-router-dom';
import {
    SortingState,
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    getSortedRowModel,
    useReactTable
} from '@tanstack/react-table';
import { SetStateAction, useState } from 'react';
import { randomTransactionData } from '../../api/test/randomTransactionsData';
import React from 'react';
import { TransactionsFilters } from '../../api/types';
import { useGetAllTransactions } from '../../api/queries';
import { getAllTransactionResponse } from '../../api/interfaces';

declare global {
    interface Window {
        test(length: number): void;
    }
}

interface Props {
    project: {
        name: string;
        id: string;
        api_base: string;
        slug: string;
    };
    lengthTransactionRequest: (length: SetStateAction<string>) => void;
}
interface TableProps {
    tableData: getAllTransactionResponse['items'];
    project: {
        name: string;
        id: string;
        api_base: string;
        slug: string;
    };
}

type transaction = {
    timestamp: string;
    prompt: string;
    response: string;
    model: string;
    tags: string[];
    // usage: {
    //     prompt_tokens: number;
    //     completion_tokens: number;
    //     total_tokens: number;
    // };
    more: JSX.Element;
};

const columnHelper = createColumnHelper<transaction>();
const columns = [
    columnHelper.accessor('timestamp', {
        header: 'timestamp',
        cell: (v) => {
            const d = new Date(v.getValue());
            return `${d.toLocaleDateString()}\n${d.getHours()}:${String(d.getMinutes()).padStart(
                2,
                '0'
            )}`;
        },
        sortingFn: (a, b, id) => {
            const dateA = new Date(a.getValue(id));
            const dateB = new Date(b.getValue(id));
            if (dateA > dateB) return 1;
            else if (dateA == dateB) return 0;
            else return -1;
        }
    }),
    columnHelper.accessor('prompt', {
        header: () => 'Prompt',
        cell: (v) => {
            const value = v.getValue();
            if (value.length > 30) return value.substring(0, 27) + '...';
            return value;
        },
        size: 300,
        sortingFn: 'text'
    }),
    columnHelper.accessor('response', {
        header: () => <span>Response</span>,
        cell: (v) => {
            const value = v.getValue();
            if (value.length > 25) return value.substring(0, 22) + '...';
            return value;
        },
        size: 300,
        sortingFn: 'text'
    }),
    columnHelper.accessor('model', {
        header: 'Model',
        cell: (v) => v.getValue(),
        sortingFn: 'text',
        size: 200
    }),
    columnHelper.accessor('tags', {
        header: 'Tags',
        cell: (v) => `${v.getValue()}`
    }),
    // columnHelper.accessor('usage', {
    //     header: 'Usage',
    //     cell: (v) => {
    //         const { prompt_tokens, completion_tokens } = v.getValue();
    //         return (
    //             <div>
    //                 <p>{prompt_tokens}+</p>
    //                 <p>{completion_tokens}</p>
    //             </div>
    //         );
    //     },
    //     sortingFn: (a, b, id) => {
    //         const t1 = (a.getValue(id) as transaction['usage']).total_tokens;
    //         const t2 = (b.getValue(id) as transaction['usage']).total_tokens;
    //         if (t1 > t2) return 1;
    //         else if (t1 == t2) return 0;
    //         else return -1;
    //     },
    //     size: 50
    // }),
    columnHelper.accessor('more', {
        header: 'More',
        cell: (v) => v.getValue(),
        size: 50,
        enableSorting: false,
        enableGlobalFilter: false
    })
];
const Table: React.FC<TableProps> = ({ tableData, project }) => {
    const [sorting, setSorting] = useState<SortingState>([]);
    const [data, setData] = useState<transaction[]>(
        tableData.map((tr) => ({
            timestamp: tr.timestamp,
            tags: tr.tags,
            prompt: (() => {
                let str = '';
                if (tr.request.content.messages)
                    tr.request.content.messages.map((m) => (str += `{${m.role}}: ${m.content}\n`));
                else
                    try {
                        tr.request.content.prompt.map((p, id) => (str += `{prompt_${id}}: ${p}\n`));
                    } catch (err) {
                        str += `${err}`;
                    }
                return str;
            })(),
            response: (() => {
                let str = '';
                try {
                    tr.response.content.choices.map((c) => {
                        if (c.message) str += `{${c.message.role}}: ${c.message.content}\n`;
                        else str += `{response_${c.index}}: ${c.text}\n`;
                    });
                } catch (err) {
                    str = `${err}`;
                }

                return str;
            })(),
            model: (() => {
                return `${tr.response.content.model}`; //\n(${tr.request.url})`;
            })(),
            // usage: tr.response.content.usage,
            more: (
                <Link
                    className="underline"
                    id={tr.id}
                    to={`/transactions/${tr.id}`}
                    state={{
                        project: {
                            name: project.name,
                            api_base: project.api_base,
                            slug: project.slug
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
        state: { sorting },
        onSortingChange: setSorting,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel()
    });
    window.test = (length: number) => {
        setData(randomTransactionData(length || 5));
    };
    return (
        <div className="table__transactions">
            <table>
                <thead>
                    {table.getHeaderGroups().map((hGroup) => (
                        <tr key={hGroup.id}>
                            {hGroup.headers.map((h) => (
                                <th
                                    key={h.id}
                                    style={{ width: `${h.getSize()}px` }}
                                    onClick={h.column.getToggleSortingHandler()}
                                >
                                    <div
                                        className={`content ${
                                            { asc: 'sort-asc', desc: 'sort-desc' }[
                                                h.column.getIsSorted() as string
                                            ] ?? ''
                                        }`}
                                    >
                                        {h.isPlaceholder
                                            ? null
                                            : flexRender(h.column.columnDef.header, h.getContext())}
                                    </div>
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>

                <tbody>
                    {table.getRowModel().rows.map((row) => (
                        <tr key={row.id}>
                            {row.getVisibleCells().map((cell) => (
                                <td key={cell.id}>
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                </td>
                            ))}
                        </tr>
                    ))}
                    {(() => {
                        const rows = Array.from(
                            { length: 5 - table.getRowModel().rows.length },
                            () => Array.from({ length: 6 }, (_, i) => i)
                        );
                        return rows.map((r, i) => (
                            <tr key={i}>
                                {r.map((_, j) => (
                                    <td key={i + j}>&nbsp;</td>
                                ))}
                            </tr>
                        ));
                    })()}
                </tbody>
            </table>
        </div>
    );
};
const LatestTransactions: React.FC<Props> = ({ project, lengthTransactionRequest }) => {
    const filters: TransactionsFilters = {
        // page: 1
        page_size: 5,
        project_id: project.id
    };
    const transactions = useGetAllTransactions(filters);

    if (transactions.isLoading)
        return (
            <>
                <div>loading...</div>
            </>
        );
    if (transactions.isError)
        return (
            <>
                <div>An error has occurred</div>
                {console.error(transactions.error)}
                <span>{transactions.error.message}</span>
            </>
        );
    if (transactions.isSuccess) {
        lengthTransactionRequest(`${transactions.data.data.total_elements}`);
        return <Table tableData={transactions.data.data.items} project={project} />;
    }
};
export default LatestTransactions;
