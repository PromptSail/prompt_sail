import { useState } from 'react';
import { transaction } from '../types';
import {
    SortingState,
    flexRender,
    getCoreRowModel,
    getSortedRowModel,
    useReactTable
} from '@tanstack/react-table';
import { getAllTransactionResponse } from '../../../api/interfaces';
import { Link } from 'react-router-dom';
import { columns } from '../columns';
import { randomTransactionData } from '../../../api/test/randomTransactionsData';

interface Props {
    tableData: getAllTransactionResponse['items'];
    project: {
        name: string;
        id: string;
        api_base: string;
        slug: string;
    };
}

const LatestTransactionsTable: React.FC<Props> = ({ tableData, project }) => {
    const [sorting, setSorting] = useState<SortingState>([]);
    const [data, setData] = useState<transaction[]>(
        tableData.map((tr) => ({
            time: tr.request_time,
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
        <div className="table__LatestTransactions">
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

export default LatestTransactionsTable;
