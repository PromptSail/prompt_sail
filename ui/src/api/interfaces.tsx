export interface addProjectRequest {
    name: string;
    slug: string;
    description: string;
    ai_providers: {
        deployment_name: string;
        slug: string;
        api_base: string;
        description: string;
        provider_name: string;
    }[];
    tags: string[];
    org_id: string;
}

export interface updateProjectRequest extends addProjectRequest {}

export interface getAllProjects {
    id: string;
    name: string;
    slug: string;
    description: string;
    ai_providers: {
        deployment_name: string;
        slug: string;
        api_base: string;
        description: string;
        provider_name: string;
    }[];
    tags: string[];
    org_id: string | undefined;
    total_transactions: number;
    total_tokens_usage: number;
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
    provider: string;
    model: string;
    type: string;
    os: string | null;
    input_tokens: number | null;
    output_tokens: number | null;
    library: string;
    status_code: number;
    message: string | null;
    prompt: string;
    error_message: string | null;
    request_time: string;
    response_time: string;
    generation_speed: number;
    input_cost: number;
    output_cost: number;
    total_cost: number;
    tags: string[];
}
export interface getAllTransactionResponse {
    items: getTransactionResponse[];
    page_index: number;
    page_size: number;
    total_pages: number;
    total_elements: number;
}
export interface getProviders {
    provider_name: string;
    api_base_placeholder: string;
}
