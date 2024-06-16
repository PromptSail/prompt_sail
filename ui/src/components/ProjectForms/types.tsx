import { addProjectRequest } from '../../api/interfaces';

export const FormikValuesTemplate: addProjectRequest = {
    name: '',
    slug: '',
    description: '',
    ai_providers: [
        {
            deployment_name: '',
            slug: '',
            api_base: '',
            description: '',
            provider_name: ''
        }
    ],
    tags: [] as string[],
    org_id: '',
    owner: ''
};
