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
};

export type Statistics_TransactionsCount = {
    project_id: string;
    date_from?: string;
    date_to?: string;
    peroid?: 'monthly' | 'weekly' | 'daily' | 'hourly' | 'minutely';
};
