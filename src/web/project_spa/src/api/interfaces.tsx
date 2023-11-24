export interface addProjectRequest {
    name: string;
    slug: string;
    description: string;
    ai_providers: [
        {
            api_base: string;
            provider_name: string;
            model_name: string;
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
            model_name: string;
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
            model_name: string;
        }
    ];
    tags: string[];
    org_id: string;
}
