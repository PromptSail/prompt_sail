import { createColumnHelper } from '@tanstack/react-table';
import { transaction } from './types';

const columnHelper = createColumnHelper<transaction>();
export const columns = [
    columnHelper.accessor('time', {
        header: 'time',
        cell: (v) => {
            const d = new Date(v.getValue() + 'Z');
            return `${d.toLocaleDateString()}\n${d.getHours()}:${String(d.getMinutes()).padStart(
                2,
                '0'
            )}:${String(d.getSeconds()).padStart(2, '0')}`;
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
