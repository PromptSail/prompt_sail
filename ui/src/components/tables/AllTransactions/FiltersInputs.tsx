import { SetStateAction, useRef } from 'react';
import { TransactionsFilters } from '../../../api/types';
import { ProjectSelect } from '../types';
import { Button, Form, InputGroup } from 'react-bootstrap';
import DateRangePicker from 'rsuite/esm/DateRangePicker';

export const FiltersInputs: React.FC<{
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    page: number;
    totalPages: number;
    totalElements: number;
    projectNames: ProjectSelect[];
}> = ({ page, totalPages, totalElements, setFilters, projectNames }) => {
    const setPage = (val: number) => {
        setFilters((old) => ({
            ...old,
            page: `${val}`
        }));
    };
    const tagsInput = useRef(null);
    return (
        <div className="table__filters">
            <div className="inputs">
                <div className="row">
                    <div className="project_select">
                        <Form.Select
                            size="sm"
                            aria-label="Select project"
                            onChange={(v) => {
                                const project_id = v.currentTarget.value;
                                setFilters((old) => ({
                                    ...old,
                                    project_id,
                                    page: '1'
                                }));
                            }}
                        >
                            {projectNames.length > 0 && (
                                <>
                                    <option value="">Select project</option>
                                    {projectNames.map((el) => (
                                        <option key={el.id} value={el.id}>
                                            {el.name}
                                        </option>
                                    ))}
                                </>
                            )}
                            {projectNames.length == 0 && (
                                <>
                                    <option value="">No projects found</option>
                                </>
                            )}
                        </Form.Select>
                    </div>
                    <div className="tags">
                        <InputGroup size="sm">
                            <Form.Control
                                placeholder="tags"
                                aria-label="tags"
                                aria-describedby="basic-addon2"
                                ref={tagsInput}
                            />
                            <Button
                                variant="primary"
                                id="tagsSelect"
                                onClick={() => {
                                    const tags = (
                                        tagsInput.current as unknown as HTMLInputElement
                                    ).value.replace(/ /g, '');
                                    setFilters((old) => ({
                                        ...old,
                                        tags,
                                        page: '1'
                                    }));
                                }}
                            >
                                Search
                            </Button>
                        </InputGroup>
                    </div>
                </div>
                <div className="row">
                    <DateRangePicker
                        format="yyyy-MM-dd HH:mm:ss"
                        placeholder="Select date range"
                        onChange={(v) => {
                            if (v != null) {
                                setFilters((old) => ({
                                    ...old,
                                    date_from: v[0].toISOString(),
                                    date_to: v[1].toISOString(),
                                    page: '1'
                                }));
                            } else {
                                setFilters((old) => ({ ...old, date_from: '', date_to: '' }));
                            }
                        }}
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
                    <div className="page_size">
                        <select
                            onChange={(v) => {
                                const page_size = v.currentTarget.value;
                                setFilters((old) => ({
                                    ...old,
                                    page_size,
                                    page: '1'
                                }));
                            }}
                            defaultValue={20}
                        >
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="5">5</option>
                            <option value="10">10</option>
                            <option value="15">15</option>
                            <option value="20">20</option>
                            <option value="30">30</option>
                        </select>
                    </div>
                    <span>{page < 0 ? 'Loading...' : `${totalElements} rows`}</span>
                </div>
            </div>
        </div>
    );
};
