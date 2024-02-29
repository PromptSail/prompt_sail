import { getAllTransactionResponse } from '../../../api/interfaces';
import { transaction } from '../types';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { randomTransactionData } from '../../../api/test/randomTransactionsData';
import { columns } from '../columns';
import iconSrc from '../../../assets/icons/box-arrow-up-right.svg';
import { ReactSVG } from 'react-svg';

interface Props {
    tableData: getAllTransactionResponse['items'];
    pageSize: number;
}

const AllTransactionsTable: React.FC<Props> = ({ tableData, pageSize }) => {
    const [data, setData] = useState<transaction[]>(
        tableData.map((tr) => ({
            time: tr.request_time,
            tags: tr.tags,
            prompt: tr.prompt,
            response: `${tr.message}`,
            model: tr.model,
            more: (
                <Link className="link" target="_blank" id={tr.id} to={`/transactions/${tr.id}`}>
                    <span>Details</span>&nbsp;
                    <ReactSVG src={iconSrc} />
                </Link>
            )
        }))
    );
    window.test = (length: number) => {
        setData(randomTransactionData(length || 5));
    };
    return (
        <>
            {/* <div className="table__AllTransactions">
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
                                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                    </td>
                                ))}
                            </tr>
                        ))}
                        {(() => {
                            const rows = Array.from(
                                {
                                    length:
                                        (pageSize < 0 ? 20 : pageSize) -
                                        table.getRowModel().rows.length
                                },
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
            </div> */}
        </>
    );
};

export default AllTransactionsTable;
