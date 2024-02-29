import { useEffect, useState } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useSearchParams } from 'react-router-dom';
import FilterProject from '../filters/FilterProject';
import FilterTags from '../filters/FilterTags';
import FilterDates from '../filters/FilterDates';
import FilterPageSize from '../filters/FilterPageSize';
import { useGetAllTransactions } from '../../../api/queries';
import AllTransactionsTable from './AllTransactionsTable';

export const TableWrapper: React.FC = () => {
    const [params, setParams] = useSearchParams();
    const [filters, setFilters] = useState<TransactionsFilters>({
        project_id: params.get('project_id') || '',
        tags: params.get('tags') || '',
        date_from: params.get('date_from') || '',
        date_to: params.get('date_to') || '',
        page_size: params.get('page_size') || '10'
    });
    const transactions = useGetAllTransactions(filters);
    const [{ page, totalPages, totalElements }, setPagesInfo] = useState({
        page: -1,
        totalPages: -1,
        totalElements: -1
    });
    useEffect(() => {
        if (transactions.isSuccess) {
            setPagesInfo({
                page: transactions.data.data.page_index,
                totalPages: transactions.data.data.total_pages,
                totalElements: transactions.data.data.total_elements
            });
        }
    }, [transactions.status]);
    const setPage = (val: number) => {
        setFilters((old) => ({
            ...old,
            page: `${val}`
        }));
    };
    const setNewParam = (param: { [key: string]: string }) => {
        const newParam = new URLSearchParams(params);
        for (const key in param) {
            if (Object.prototype.hasOwnProperty.call(param, key)) {
                param[key].length > 0 ? newParam.set(key, param[key]) : newParam.delete(key);
            }
        }
        setParams(newParam);
    };
    return (
        <div className="table__wrapper">
            <div className="table__filters">
                <div className="inputs">
                    <FilterProject
                        projectId={filters.project_id}
                        setFilters={setFilters}
                        setNewParam={setNewParam}
                    />
                    <FilterDates
                        params={params}
                        setParams={setParams}
                        setFilters={setFilters}
                        setNewParam={setNewParam}
                    />
                    <FilterTags
                        tags={filters.tags}
                        setFilters={setFilters}
                        setNewParam={setNewParam}
                    />
                </div>
                <div className="page">
                    <div className="info">
                        <span>{page < 0 ? 'Loading...' : `${page} of ${totalPages}`}</span>
                        <FilterPageSize
                            pageSize={filters.page_size}
                            setFilters={setFilters}
                            setNewParam={setNewParam}
                        />
                        <span>{page < 0 ? 'Loading...' : `${totalElements} rows`}</span>
                    </div>
                    <div className="buttons">
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(1)}
                            disabled={page == 1}
                        >{`<<`}</button>
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(page - 1)}
                            disabled={page == 1}
                        >{`<`}</button>
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(page + 1)}
                            disabled={page >= totalPages}
                        >{`>`}</button>
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(totalPages)}
                            disabled={page >= totalPages}
                        >{`>>`}</button>
                    </div>
                </div>
            </div>
            {transactions.isError && (
                <>
                    {console.error(transactions.error)}
                    <div>Error</div>
                </>
            )}
            {transactions.isLoading && <div>Loading...</div>}
            {transactions.isSuccess && (
                <AllTransactionsTable
                    pageSize={Number(filters.page_size) || -1}
                    tableData={transactions.data.data.items}
                />
            )}
            <div className="table__filters_footer">
                <div className="page">
                    <div className="info">
                        <span className="my-auto">
                            {page < 0 ? 'Loading...' : `${page} of ${totalPages}`}
                        </span>
                        <FilterPageSize
                            pageSize={filters.page_size}
                            setFilters={setFilters}
                            setNewParam={setNewParam}
                        />
                        <span className="my-auto">
                            {page < 0 ? 'Loading...' : `${totalElements} rows`}
                        </span>
                    </div>
                    <div className="buttons">
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(1)}
                            disabled={page == 1}
                        >{`<<`}</button>
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(page - 1)}
                            disabled={page == 1}
                        >{`<`}</button>
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(page + 1)}
                            disabled={page >= totalPages}
                        >{`>`}</button>
                        <button
                            style={{ background: '#71aaff' }}
                            onClick={() => setPage(totalPages)}
                            disabled={page >= totalPages}
                        >{`>>`}</button>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default TableWrapper;
