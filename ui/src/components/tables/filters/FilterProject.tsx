import { SetStateAction } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllProjects } from '../../../api/queries';
import { Select } from 'antd';

interface Props {
    defaultValue: string | undefined;
    setFilters: (args: SetStateAction<TransactionsFilters>) => void;
    setProject: (project_id: string) => void;
}
const FilterProject: React.FC<Props> = ({ defaultValue, setFilters, setProject }) => {
    const projects = useGetAllProjects();
    if (projects.isLoading)
        return (
            <Select
                defaultValue={defaultValue}
                loading
                style={{ width: 150 }}
                options={[{ value: '', label: 'Select project' }]}
            />
        );
    if (projects.isError)
        return (
            <Select
                defaultValue={defaultValue}
                style={{ width: 150 }}
                options={[
                    { value: '', label: 'Select project' },
                    { value: '', label: `${projects.error.code}: ${projects.error.message}` }
                ]}
            />
        );
    if (projects.isSuccess) {
        const options =
            projects.data.length > 0
                ? [{ value: '', label: 'Select project' }]
                : [{ value: '', label: 'No projects found' }];
        projects.data.map((el) => options.push({ value: el.id, label: el.name }));

        return (
            <Select
                defaultValue={defaultValue}
                onChange={(e) => {
                    setFilters((old) => ({ ...old, project_id: e }));
                    setProject(e);
                }}
                style={{ width: 150 }}
                options={options}
            />
        );
    }
};
export default FilterProject;
