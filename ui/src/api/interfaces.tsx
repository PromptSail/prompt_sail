export interface addProjectRequest {
    name: string;
    slug: string;
    description: string;
    ai_providers: {
        deployment_name: string;
        api_base: string;
        description: string;
        provider_name: string;
    }[];
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

export interface getAllProjects {
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
    org_id: string | undefined;
}

export interface getProjectResponse extends getAllProjects {}

export interface getTransactionResponse {
    id: string;
    project_id: string;
    project_name: string;
    request: {
        content: {
            input?: string;
            model?: string;
            messages?: [
                {
                    content: string;
                    role: string;
                }
            ];
        };
        extensions: {
            timeout: {
                connect: number;
                pool: number;
                read: number;
                write: number;
            };
        };
        headers: Headers;
        host: string;
        method: string;
        url: string;
        [key: string]: any;
    };
    response: {
        [key: string]: any;
    };
    model: string;
    type: string;
    os: string | null;
    token_usage: number;
    library: string;
    status_code: number;
    message: string | null;
    prompt: string;
    error_message: string | null;
    request_time: string;
    response_time: string;
    tags: string[];
}
export interface getAllTransactionResponse {
    items: getTransactionResponse[];
    page_index: number;
    page_size: number;
    total_pages: number;
    total_elements: number;
}
