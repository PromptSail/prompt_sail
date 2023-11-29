import { getProjectResponse } from './interfaces';
const default_getProjectRespons: getProjectResponse = {
    id: '',
    name: '',
    slug: '',
    description: '',
    ai_providers: [
        {
            api_base: '',
            provider_name: '',
            model_name: ''
        }
    ],
    tags: [],
    org_id: '',
    transactions: [
        {
            id: '',
            project_id: '',
            timestamp: '',
            request: {
                url: '',
                content: {
                    prompt: []
                }
            },
            response: {
                headers: {},
                status_code: '',
                content: {
                    model: '',
                    usage: {
                        prompt_tokens: 0,
                        completion_tokens: 0,
                        total_tokens: 0
                    },
                    choices: [
                        {
                            index: '',
                            text: '',
                            message: {
                                role: '',
                                content: ''
                            }
                        }
                    ]
                }
            }
        }
    ]
};

export { default_getProjectRespons };
