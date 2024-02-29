import { SetStateAction } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { useGetAllProjects } from '../../../api/queries';

interface Props {
    projectId: string | undefined;
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    setNewParam: (param: { [key: string]: string }) => void;
}
const FilterProject: React.FC<Props> = ({ projectId, setFilters, setNewParam }) => {
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
        return (
            <div className="project_select">
                <select
                    aria-label="Select project"
                    value={projectId}
                    onChange={(v) => {
                        const project_id = v.currentTarget.value;
                        setFilters((old) => ({
                            ...old,
                            project_id,
                            page: '1'
                        }));
                        setNewParam({ project_id });
                    }}
                >
                    {projects.data.length > 0 && (
                        <>
                            <option value="">Select project</option>
                            {projects.data.map((el) => (
                                <option key={el.id} value={el.id}>
                                    {el.name}
                                </option>
                            ))}
                        </>
                    )}
                    {projects.data.length == 0 && (
                        <>
                            <option value="">No projects found</option>
                        </>
                    )}
                </select>
            </div>
        );
    }
};
export default FilterProject;
