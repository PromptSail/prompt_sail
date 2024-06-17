import { createContext, useState, useContext, ReactNode } from 'react';
import Page500 from '../components/errorPages/page500';
import { AxiosInterceptor } from '../api/client';

const ErrorContext = createContext<{
    hasServerError: boolean;
    setHasServerError: (arg: boolean) => void;
}>({ hasServerError: false, setHasServerError: () => null });

export const ErrorProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [hasServerError, setHasServerError] = useState(false);
    return (
        <ErrorContext.Provider value={{ hasServerError, setHasServerError }}>
            <AxiosInterceptor>{hasServerError ? <Page500 /> : children}</AxiosInterceptor>
        </ErrorContext.Provider>
    );
};

export const useError = () => useContext(ErrorContext);
