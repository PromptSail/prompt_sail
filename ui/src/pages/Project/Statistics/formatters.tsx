export const dateFormatter = (val: string) => {
    const date = new Date(val).toLocaleString('en-US', {
        month: '2-digit',
        day: '2-digit',
        year: '2-digit'
    });
    return `${date}`;
};
