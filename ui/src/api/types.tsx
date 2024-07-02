import { Period } from '../pages/Project/Statistics/Statistics';
import { getTransactionResponse } from './interfaces';

export type TransactionsFilters = {
    page?: string;
    page_size?: string;
    tags?: string;
    date_from?: string;
    date_to?: string;
    project_id?: string;
    sort_field?: keyof getTransactionResponse | '';
    sort_type?: 'asc' | '';
    status_codes?: string;
    provider_models?: string;
};

export type StatisticsParams = {
    project_id: string;
    date_from?: string;
    date_to?: string;
    period?: Period;
};
