import { Payload, NameType } from 'recharts/types/component/DefaultTooltipContent';

export const dateFormatter = (val: string) => {
    const date = new Date(val).toLocaleString('en-US', {
        month: '2-digit',
        day: '2-digit',
        year: '2-digit'
    });
    return `${date}`;
};

export const costFormatter = (val: number) => {
    return '$ ' + val.toFixed(4);
};
export const costTooltip = (val: number) => {
    return '$ ' + val.toFixed(4);
};

export const customSorter = (item: Payload<number, NameType>) => {
    const key = item.dataKey;
    const payloadKeys = Object.keys(item.payload);
    for (let i = 0; i < payloadKeys.length; i++) {
        if (payloadKeys[i] === key) {
            return -i;
        }
    }
    return 0;
};
