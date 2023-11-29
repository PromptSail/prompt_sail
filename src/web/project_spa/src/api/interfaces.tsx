export interface addProjectRequest {
    name: string;
    slug: string;
    description: string;
    ai_providers: [
        {
            api_base: string;
            provider_name: string;
            ai_model_name: string;
        }
    ];
    tags: string[];
    org_id: string;
}

export interface updateProjectRequest {
    id: string;
    name: string;
    slug: string;
    description: string;
    ai_providers: [
        {
            api_base: string;
            provider_name: string;
            ai_model_name: string;
        }
    ];
    tags: string[];
    org_id: string;
}

export interface getProjectResponse {
    id: string;
    name: string;
    slug: string;
    description: string;
    ai_providers: [
        {
            api_base: string;
            provider_name: string;
            ai_model_name: string;
        }
    ];
    tags: string[];
    org_id: string;
    transactions: [
        {
            id: string;
            project_id: string;
            timestamp: string;
            request: {
                url: string;
                content: {
                    messages?: [
                        {
                            role: string;
                            content: string;
                        }
                    ];
                    prompt: string[];
                };
                [key: string]: unknown;
            };
            response: {
                headers: { [key: string]: string };
                status_code: string;
                content: {
                    model: string;
                    usage: {
                        prompt_tokens: number;
                        completion_tokens: number;
                        total_tokens: number;
                    };
                    choices: [
                        {
                            index: string;
                            text: string;
                            message: {
                                role: string;
                                content: string;
                            };
                        }
                    ];
                };
                [key: string]: unknown;
            };
        }
    ];
}
