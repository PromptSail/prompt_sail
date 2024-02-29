import { SetStateAction, useRef } from 'react';
import { TransactionsFilters } from '../../../api/types';

interface Props {
    tags: string | undefined;
    setFilters: (length: SetStateAction<TransactionsFilters>) => void;
    setNewParam: (param: { [key: string]: string }) => void;
}

const FilterTags: React.FC<Props> = ({ tags, setFilters, setNewParam }) => {
    const tagsInput = useRef(null);
    return (
        <div className="tags">
            {/* <InputGroup size="sm">
                <Form.Control
                    placeholder="tags"
                    aria-label="tags"
                    aria-describedby="basic-addon2"
                    ref={tagsInput}
                    defaultValue={tags}
                />
                <Button
                    style={{ background: '#71aaff' }}
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
                        setNewParam({ tags });
                    }}
                >
                    Search
                </Button>
            </InputGroup> */}
        </div>
    );
};
export default FilterTags;
