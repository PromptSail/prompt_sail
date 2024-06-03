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
    total_cost: number;
    total_transactions: number;
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
    messages:
        | {
              role: string;
              content: string;
          }[]
        | null;
    last_message: string;
    prompt: string;
    error_message: string | null;
    request_time: string;
    response_time: string;
    generation_speed: number;
    input_cost: number;
    output_cost: number;
    total_cost: number | null;
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
export interface getStatisticsTransactionsCount {
    date: string;
    status_200: number;
    status_300: number;
    status_400: number;
    status_500: number;
    total_transactions: number;
}
export interface getStatisticsTransactionsCost {
    date: string;
    records: {
        provider: string;
        model: string;
        total_input_tokens: number;
        total_output_tokens: number;
        input_cumulative_total: number;
        output_cumulative_total: number;
        total_transactions: number;
        total_cost: number;
    }[];
}
export interface getStatisticsTransactionsSpeed {
    date: string;
    records: {
        provider: string;
        model: string;
        mean_latency: number;
        tokens_per_second: number;
        total_transactions: number;
    }[];
}
export interface getLoggedUser {
    external_id: string;
    email: string;
    organization: string;
    given_name: string;
    family_name: string;
    picture: string;
    issuer: string;
}
