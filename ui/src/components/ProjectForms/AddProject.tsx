import { useAddProject } from '../../api/queries';
import { addProjectRequest } from '../../api/interfaces';
import { addProjectSchema } from '../../api/formSchemas';
import ProjectForm from '../../pages/ProjectForm';
import { FormikValues } from './types';
import { Button } from 'react-bootstrap';

const AddProject: React.FC = () => {
    const addProject = useAddProject();
    const submit = async ({
        name = '',
        slug = '',
        description = '',
        ai_providers: [{ api_base = '', provider_name = '', ai_model_name = '' }],
        tags = '',
        org_id = ''
    }: typeof FormikValues) => {
        const reqValues: addProjectRequest = {
            name,
            slug,
            description,
            ai_providers: [
                {
                    api_base,
                    provider_name,
                    ai_model_name
                }
            ],
            tags: tags.replace(/\s/g, '').split(','),
            org_id
        };
        addProject.mutateAsync({ data: reqValues }).then(() => {
            // queryToRefetch.refetch();
        });
    };
    return (
        <div className="project__add">
            <ProjectForm onSubmit={submit} validationSchema={addProjectSchema} />
            <Button>Add</Button>
            {/* <ProjectForm queryToRefetch={undefined} /> */}
        </div>
    );
};
export default AddProject;
