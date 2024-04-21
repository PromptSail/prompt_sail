import { Payload, NameType } from 'recharts/types/component/DefaultTooltipContent';
import { Period } from './Statistics';

export const dateFormatter = (val: string | number, granularity: Period | undefined) => {
    const date = new Date(val);
    const convertedDate = new Date(date + 'Z').toLocaleString(
        'en-US',
        granularity == Period.Hourly || granularity == Period.Minutely
            ? {
                  hour: '2-digit',
                  minute: '2-digit'
              }
            : { month: '2-digit', day: '2-digit', year: '2-digit' }
    );
    return `${convertedDate}`;
};
export const dataRounding = (val: number, round: number) => {
    return val.toFixed(round);
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
