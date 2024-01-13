type transaction = {
    time: string;
    tags: string[];
    prompt: string;
    response: string;
    model: string;
    usage: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
    more: JSX.Element;
};
export const randomTransactionData = (length: number) => {
    const test_data: transaction[] = [];
    for (let i = 0; i <= length; i++) {
        const random = Math.random() * 1699999999999;
        test_data[i] = {
            time: new Date(random).toString(),
            tags: ['a', 'b', 'c'],
            prompt: makeStr(Math.random() * 20),
            response: makeStr(Math.random() * 20),
            model: makeStr(Math.random() * 10),
            usage: (() => {
                const a = Math.round(Math.random() * 20);
                const b = Math.round(Math.random() * 20);
                return {
                    prompt_tokens: a,
                    completion_tokens: b,
                    total_tokens: a + b
                };
            })(),
            more: <span>Details</span>
        };
    }
    return test_data;
};

const makeStr = (length: number) => {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
};
