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
            <ErrorProvider>
                <Context.Provider value={{ notification: noteApi, modal: modalApi, config }}>
                    {noteContextHolder}
                    {modalContextHolder}
                    {isLogged && (
                        <Layout>
                            <Sidebar setLoginState={setLoginState} />
                            <Layout className="h-screen overflow-auto">
                                <Routes>
                                    <Route path="/" element={<Dashboard />} />
                                    <Route
                                        path="/projects/:projectId/edit-project-details"
                                        element={<Project.Update />}
                                    />
                                    <Route path="/projects/:projectId" element={<Project />} />
                                    <Route
                                        path="/projects/add"
                                        element={<Project.Add notification={noteApi} />}
                                    />
                                    <Route path="/transactions" element={<Transactions />} />
                                    <Route
                                        path="/transactions/:transactionId"
                                        element={<Transaction />}
                                    />
                                    <Route path="*" element={<Navigate to="/" />} />
                                </Routes>
                            </Layout>
                        </Layout>
                    )}
                    {!isLogged && (
                        <Layout className="h-screen">
                            <Routes>
                                <Route
                                    path="/signin"
                                    element={<Signin setLoginState={setLoginState} />}
                                />
                                <Route path="*" element={<Navigate to="/signin" />} />
                            </Routes>
                        </Layout>
                    )}
                </Context.Provider>
            </ErrorProvider>
        </ConfigProvider>
    );
};

export default App;
