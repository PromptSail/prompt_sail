import { ReactNode, SetStateAction, useEffect } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { Button } from 'react-bootstrap';
import { useSearchParams } from 'react-router-dom';
import FilterProject from '../filters/FilterProject';
import FilterTags from '../filters/FilterTags';
import FilterDates from '../filters/FilterDates';
import FilterPageSize from '../filters/FilterPageSize';

export const TableWrapper: React.FC<{
    children: ReactNode;
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    filters: TransactionsFilters;
    page: number;
    totalPages: number;
    totalElements: number;
}> = ({ children, page, totalPages, totalElements, filters, setFilters }) => {
    const [params, setParams] = useSearchParams();
    useEffect(() => {
        setFilters((old) => ({
            ...old,
            project_id: params.get('project_id') || '',
            tags: params.get('tags') || '',
            date_from: params.get('date_from') || '',
            date_to: params.get('date_to') || '',
            page_size: params.get('page_size') || '20'
        }));
    }, []);
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
                    <div className="row">
                        <FilterProject
                            projectId={filters.project_id}
                            setFilters={setFilters}
                            setNewParam={setNewParam}
                        />
                        <FilterTags
                            tags={filters.tags}
                            setFilters={setFilters}
                            setNewParam={setNewParam}
                        />
                    </div>
                    <div className="row">
                        <FilterDates
                            params={params}
                            setParams={setParams}
                            setFilters={setFilters}
                            setNewParam={setNewParam}
                        />
                    </div>
                </div>
                <div className="page">
                    <div className="row">
                        <Button
                            size="sm"
                            onClick={() => setPage(1)}
                            disabled={page == 1}
                        >{`<<`}</Button>
                        <Button
                            size="sm"
                            onClick={() => setPage(page - 1)}
                            disabled={page == 1}
                        >{`<`}</Button>
                        <Button
                            size="sm"
                            onClick={() => setPage(page + 1)}
                            disabled={page >= totalPages}
                        >{`>`}</Button>
                        <Button
                            size="sm"
                            onClick={() => setPage(totalPages)}
                            disabled={page >= totalPages}
                        >{`>>`}</Button>
                    </div>
                    <div className="row">
                        <span>{page < 0 ? 'Loading...' : `${page} of ${totalPages}`}</span>
                        <FilterPageSize
                            pageSize={filters.page_size}
                            setFilters={setFilters}
                            setNewParam={setNewParam}
                        />
                        <span>{page < 0 ? 'Loading...' : `${totalElements} rows`}</span>
                    </div>
                </div>
            </div>
            {children}
            <div className="table__filters_footer">
                <span className="my-auto">
                    {page < 0 ? 'Loading...' : `${page} of ${totalPages}`}
                </span>
                <FilterPageSize
                    pageSize={filters.page_size}
                    setFilters={setFilters}
                    setNewParam={setNewParam}
                />
                <span className="my-auto">{page < 0 ? 'Loading...' : `${totalElements} rows`}</span>
                <div className="row">
                    <div>
                        <Button
                            size="sm"
                            onClick={() => setPage(1)}
                            disabled={page == 1}
                        >{`<<`}</Button>
                        <Button
                            size="sm"
                            onClick={() => setPage(page - 1)}
                            disabled={page == 1}
                        >{`<`}</Button>
                        <Button
                            size="sm"
                            onClick={() => setPage(page + 1)}
                            disabled={page >= totalPages}
                        >{`>`}</Button>
                        <Button
                            size="sm"
                            onClick={() => setPage(totalPages)}
                            disabled={page >= totalPages}
                        >{`>>`}</Button>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default TableWrapper;
