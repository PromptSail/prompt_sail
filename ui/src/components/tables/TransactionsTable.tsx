import { Link } from 'react-router-dom';
import { getAllTransactionResponse } from '../../api/interfaces';
import {
    ColumnFiltersState,
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
import React from 'react';

declare global {
    interface Window {
        test(length: number): void;
    }
}

interface Props {
    transactions: getAllTransactionResponse;
    project: {
        name: string;
        api_base: string;
        slug: string;
    };
}

type transaction = {
    timestamp: string;
    prompt: string;
    response: string;
    model: string;
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
        },
        filterFn: (row, id, value) => {
            const rowV = new Date(row.getValue(id)).getTime();
            const start = new Date(value[0]).getTime() || rowV;
            const end = new Date(value[1]).getTime() || rowV;
            return rowV >= start && rowV <= end;
        }
    }),
    columnHelper.accessor('prompt', {
        header: () => 'Prompt',
        cell: (v) => {
            const value = v.getValue();
            console.log(value.length);
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
            console.log(value.length);
            if (value.length > 30) return value.substring(0, 27) + '...';
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
const TransactionsTable: React.FC<Props> = ({ transactions, project }) => {
    window.test = (length: number) => {
        setData(randomTransactionData(length || 5));
    };
    const [search, setSearch] = useState('');
    const [sorting, setSorting] = useState<SortingState>([]);
    const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);
    const [data, setData] = useState<transaction[]>(
        transactions.items.map((tr) => ({
            timestamp: tr.timestamp,
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
        state: { sorting, globalFilter: search, columnFilters },
        onSortingChange: setSorting,
        onColumnFiltersChange: setColumnFilters,
        onGlobalFilterChange: setSearch,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        getPaginationRowModel: getPaginationRowModel()
    });
    return (
        <>
            <div className="flex flex-row">
                <Form.Control
                    type="date"
                    onChange={(v) => {
                        const value = v.currentTarget.value;
                        table.getColumn('timestamp')?.setFilterValue((old: [string, string]) => {
                            console.log(old);
                            return [value, old?.[1]];
                        });
                    }}
                />
                <Form.Control
                    type="date"
                    onChange={(v) => {
                        const value = v.currentTarget.value;
                        table.getColumn('timestamp')?.setFilterValue((old: [string, string]) => {
                            console.log(old);
                            return [old?.[0], value];
                        });
                    }}
                />
            </div>
            <div className="overflow-x-auto p-3">
                <Form.Control
                    value={search ?? ''}
                    onChange={(obj) => {
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
                                                    : flexRender(
                                                          h.column.columnDef.header,
                                                          h.getContext()
                                                      )}
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
                                            {flexRender(
                                                cell.column.columnDef.cell,
                                                cell.getContext()
                                            )}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                            {(() => {
                                const rows = Array.from(
                                    { length: 10 - table.getRowModel().rows.length },
                                    () => Array.from({ length: 5 }, (_, i) => i)
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
            </div>
        </>
    );
};
export default TransactionsTable;
