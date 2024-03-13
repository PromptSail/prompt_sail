export const transactionTabOnLoad = () => {
    return localStorage.getItem('transactionDetailsTab') || 'basic';
};
