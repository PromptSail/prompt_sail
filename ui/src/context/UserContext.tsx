import { createContext, useContext, useEffect, useState } from 'react';
import { useGetOrganizations, useWhoami } from '../api/queries';
import { getLoggedUser } from '../api/interfaces';
import { Spin } from 'antd';
import { getStorageOrganization, setStorageOrganization } from '../storage/organization';

const User = createContext<getLoggedUser>({
    id: '',
    external_id: '',
    email: '',
    given_name: '',
    family_name: '',
    picture: '',
    issuer: '',
    is_active: false
});
const Organization = createContext<{
    organization: { id: string; name: string; type: string };
    setOrganization: (value: { id: string; name: string; type: string }) => void;
}>({
    organization: {
        id: '',
        name: '',
        type: ''
    },
    setOrganization: () => {}
});
const Loading = (
    <div className="w-screen h-screen relative">
        <Spin
            size="large"
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
        />
    </div>
);
const UserProvider: React.FC<{
    children: React.ReactNode;
}> = ({ children }) => {
    const user = useWhoami();
    if (user.isLoading) return Loading;
    if (user.isSuccess)
        return (
            <User.Provider value={user.data?.data}>
                {
                    <OrganizationsProvider userId={user.data.data.id}>
                        {children}
                    </OrganizationsProvider>
                }
            </User.Provider>
        );
};
const OrganizationsProvider: React.FC<{ children: React.ReactNode; userId: string }> = ({
    userId,
    children
}) => {
    const organizations = useGetOrganizations(userId);
    const storageOrganization = getStorageOrganization();
    const [organization, setOrganization] = useState<{ id: string; name: string; type: string }>({
        id: '',
        name: '',
        type: ''
    });
    useEffect(() => {
        if (organizations.isSuccess) {
            const data = organizations.data.data;
            const orgList = [...data.owned, ...data.as_member];
            if (!storageOrganization || orgList.every((el) => el.id !== storageOrganization.id)) {
                const { id, name, type } = orgList[0];
                setStorageOrganization(id, name, type);
                setOrganization({ id, name, type });
            } else {
                setOrganization(storageOrganization);
            }
        }
    }, [organizations.status]);
    if (organizations.isLoading) return Loading;
    if (organizations.isSuccess)
        return (
            <Organization.Provider
                value={{
                    organization,
                    setOrganization: (value) => {
                        setStorageOrganization(value.id, value.name, value.type);
                        setOrganization(value);
                    }
                }}
            >
                {children}
            </Organization.Provider>
        );
};

export default UserProvider;
export const useOrganization = () => useContext(Organization);
export const useUser = () => useContext(User);
