export const getStorageOrganization = ():
    | { id: string; name: string; type: string }
    | undefined => {
    const item = localStorage.getItem('PS_ORGANIZATION');
    return item ? JSON.parse(item) : undefined;
};

export const setStorageOrganization = (id: string, name: string, type: string): void => {
    return localStorage.setItem('PS_ORGANIZATION', JSON.stringify({ id, name, type }));
};
