import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard/Dashboard';
import Project from './pages/Project/Project';
import Transactions from './pages/Transactions';
import Sidebar from './components/Sidebar/Sidebar';
import { useEffect, useState } from 'react';
import Signin from './pages/Signin/Signin';
import { checkLogin } from './storage/login';
import { ConfigProvider, Layout, Modal, notification } from 'antd';
import Transaction from './pages/Transaction/Transaction';
import theme from './theme-light';
import { Context } from './context/Context';
import { useGetConfig } from './api/queries';
import { getConfig } from './api/interfaces';
import { ErrorProvider } from './context/ErrorContext';
import LoginProvider from './context/LoginContext';
import Page404 from './components/errorPages/page404';
import Portfolio from './pages/Portfolio/Portfolio';
import UserProvider from './context/UserContext';

const App = () => {
    const [isLogged, setLoginState] = useState(checkLogin());
    const [noteApi, noteContextHolder] = notification.useNotification();
    const [modalApi, modalContextHolder] = Modal.useModal();
    const configApi = useGetConfig();
    const [config, setConfig] = useState<getConfig | null>(null);
    useEffect(() => {
        if (configApi.isSuccess) {
            setConfig(configApi.data.data);
        }
    }, [configApi.status]);

    return (
        <ConfigProvider theme={theme}>
            <LoginProvider value={{ isLogged, setLoginState }}>
                <ErrorProvider>
                    <Context.Provider value={{ notification: noteApi, modal: modalApi, config }}>
                        {noteContextHolder}
                        {modalContextHolder}

                        {isLogged ? (
                            <UserProvider>
                                <Layout>
                                    <Sidebar />
                                    <Layout className="h-screen overflow-auto">
                                        <Routes>
                                            <Route path="/" element={<Dashboard />} />
                                            <Route
                                                path="/projects/:projectId/edit-project-details"
                                                element={<Project.Update />}
                                            />
                                            <Route
                                                path="/projects/:projectId"
                                                element={<Project />}
                                            />
                                            <Route
                                                path="/projects/add"
                                                element={<Project.Add notification={noteApi} />}
                                            />
                                            <Route
                                                path="/transactions"
                                                element={<Transactions />}
                                            />
                                            <Route
                                                path="/transactions/:transactionId"
                                                element={<Transaction />}
                                            />
                                            <Route path="/portfolio" element={<Portfolio />} />
                                            <Route path="*" element={<Page404 />} />
                                            <Route path="/signin" element={<Navigate to="/" />} />
                                        </Routes>
                                    </Layout>
                                </Layout>
                            </UserProvider>
                        ) : (
                            <Layout className="h-screen">
                                <Routes>
                                    <Route path="/signin" element={<Signin />} />
                                    <Route path="*" element={<Navigate to="/signin" />} />
                                </Routes>
                            </Layout>
                        )}
                    </Context.Provider>
                </ErrorProvider>
            </LoginProvider>
        </ConfigProvider>
    );
};
export default App;
