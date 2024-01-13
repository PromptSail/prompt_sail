export type transaction = {
    time: string;
    prompt: string;
    response: string;
    tags: string[];
    model: string;
    // usage: {
    //     prompt_tokens: number;
    //     completion_tokens: number;
    //     total_tokens: number;
    // };
    more: JSX.Element;
};

export type ProjectSelect = {
    id: string;
    name: string;
};
