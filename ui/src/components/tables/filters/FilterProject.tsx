import { SetStateAction } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllProjects } from '../../../api/queries';
import { Select } from 'antd';

interface Props {
    defaultValue: string | undefined;
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    setProject: (project_id: string) => void;
}
const FilterProject: React.FC<Props> = ({ defaultValue, setFilters, setProject }) => {
    const projects = useGetAllProjects();
    if (projects.isLoading)
        return (
            <>
                <div>...</div>
            </>
        );
    if (projects.isError)
        return (
            <>
                <div>Err</div>
                {console.error(projects.error)}
            </>
        );
    if (projects.isSuccess) {
        const options =
            projects.data.length > 0
                ? [<option value="">Select project</option>]
                : [<option value="">No projects found</option>];
        projects.data.map((el) =>
            options.push(
                <option key={el.id} value={el.id}>
                    {el.name}
                </option>
            )
        );

        return (
            <Select
                defaultValue={defaultValue}
                onChange={(e) => {
                    console.log(e);
                }}
                style={{ width: 150 }}
                options={options}
            />
        );
    }
};
export default FilterProject;
