type transaction = {
    timestamp: string;
    prompt: string;
    response: string;
    model: string;
    usage: string;
    more: JSX.Element;
};
export const randomTransactionData = (length: number) => {
    const test_data: transaction[] = [];
    for (let i = 0; i <= length; i++) {
        const random = Math.random() * 1699999999999;
        test_data[i] = {
            timestamp: (() => {
                const d = new Date(random);
                return `${d.toLocaleDateString()}\n${d.getHours()}:${d.getMinutes()}`;
            })(),
            prompt: makeStr(Math.random() * 20),
            response: makeStr(Math.random() * 20),
            model: makeStr(Math.random() * 10),
            usage: `${(Math.random() * 20).toFixed(0)}+\n${(Math.random() * 20).toFixed(0)}`,
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
