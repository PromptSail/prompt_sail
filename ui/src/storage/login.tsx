export const checkLogin = () => {
    const token = localStorage.getItem('PS_TOKEN');
    if (token !== null) return token.length > 1;
    return false;
};
