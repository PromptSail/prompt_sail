import { createContext, useContext, ReactNode } from 'react';
import { checkLogin } from '../storage/login';

const LoginContext = createContext<{
    isLogged: boolean;
    setLoginState: (arg: boolean) => void;
}>({ isLogged: checkLogin(), setLoginState: () => {} });

const LoginProvider: React.FC<{
    children: ReactNode;
    value: { isLogged: boolean; setLoginState: (arg: boolean) => void };
}> = ({ children, value }) => {
    return <LoginContext.Provider value={value}>{children}</LoginContext.Provider>;
};
export default LoginProvider;
export const useLogin = () => useContext(LoginContext);
