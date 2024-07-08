export const shortenProviderName = (provider: string) => {
    switch (provider.toLowerCase().replace(/\s/g, '')) {
        case 'OpenAI'.toLowerCase():
            return 'OAI';
        case 'Anthropic'.toLowerCase():
            return 'ANT';
        case 'GoogleVertexAI'.toLowerCase():
            return 'GGL';
        case 'AWSBedrock'.toLowerCase():
            return 'AWS';
        case 'Grog'.toLowerCase():
            return 'GRQ';
        case 'Ollama'.toLowerCase():
            return 'OLL';
        case 'Huggingface'.toLowerCase():
            return 'HGF';
        default:
            return provider.toUpperCase().substring(0, 3);
    }
};
