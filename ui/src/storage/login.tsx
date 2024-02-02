export const checkLogin = () => {
    return localStorage.getItem('login') === 'true';
};
