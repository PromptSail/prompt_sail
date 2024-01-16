import { useEffect, useState } from 'react';
import React from 'react';
import { useGetAllProjects, useGetAllTransactions } from '../api/queries';
import { TransactionsFilters } from '../api/types';
import { ProjectSelect } from '../components/tables/types';
import { FiltersInputs } from '../components/tables/AllTransactions/FiltersInputs';
import AllTransactionsTable from '../components/tables/AllTransactions/AllTransactionsTable';

declare global {
    interface Window {
        test(length: number): void;
    }
}
const AllTransactions: React.FC = () => {
    const [filters, setFilters] = useState<TransactionsFilters>({});
    const [projectsNames, setProjectsNames] = useState<ProjectSelect[]>([]);
    const transactions = useGetAllTransactions(filters);
    const [pagesInfo, setPagesInfo] = useState({
        page: -1,
        total_pages: -1,
        total_elements: -1
    });
    const projects = useGetAllProjects();
    useEffect(() => {
        if (projects.isSuccess) {
            setProjectsNames(projects.data.map((el) => ({ id: el.id, name: el.name })));
        } else if (projectsNames.length != 0) {
            setProjectsNames([]);
        }
        if (transactions.isSuccess) {
            setPagesInfo({
                page: transactions.data.data.page_index,
                total_pages: transactions.data.data.total_pages,
                total_elements: transactions.data.data.total_elements
            });
        }
    }, [projects.status, transactions.status]);
    return (
        <div className="p-5 px-20 pt-[100px] flex flex-col gap-5">
            <h2 className="text-2xl font-semibold mb-2 md:text-4xl">All Transactions</h2>
            <div>
                <FiltersInputs
                    page={pagesInfo.page}
                    totalPages={pagesInfo.total_pages}
                    totalElements={pagesInfo.total_elements}
                    projectNames={projectsNames}
                    filters={filters}
                    setFilters={setFilters}
                />
                {transactions.isLoading && (
                    <div className="overflow-x-auto p-3">
                        <div>loading...</div>
                    </div>
                )}
                {transactions.isError && (
                    <>
                        {console.error(transactions.error)}
                        <div className="overflow-x-auto p-3">
                            <span>{transactions.error.message}</span>
                        </div>
                    </>
                )}
                {transactions.isSuccess && (
                    <div className="overflow-x-auto">
                        <AllTransactionsTable
                            pageSize={Number(filters.page_size) || -1}
                            tableData={transactions.data.data.items}
                        />
                    </div>
                )}
            </div>
        </div>
    );
};
export default AllTransactions;
