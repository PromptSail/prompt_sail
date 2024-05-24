import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard/Dashboard';
import Project from './pages/Project/Project';
import Transactions from './pages/Transactions';
import Sidebar from './components/Sidebar/Sidebar';

import { useState } from 'react';
import Signin from './pages/Signin';
import { checkLogin } from './storage/login';
import { ConfigProvider, Layout, Modal, notification } from 'antd';
import Transaction from './pages/Transaction/Transaction';
import theme from './theme-light';
import { Context } from './context/Context';

const App = () => {
    const [isLogged, setLoginState] = useState(checkLogin());
    const [noteApi, noteContextHolder] = notification.useNotification();
    const [modalApi, modalContextHolder] = Modal.useModal();
    return (
        <ConfigProvider theme={theme}>
            {isLogged && (
                <Context.Provider value={{ notification: noteApi, modal: modalApi }}>
                    {noteContextHolder}
                    {modalContextHolder}
                    <Layout>
                        <Sidebar setLoginState={setLoginState} />
                        <Layout className="h-screen overflow-auto">
                            <Routes>
                                <Route path="/" element={<Dashboard />} />
                                <Route
                                    path="/projects/:projectId/update"
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
                </Context.Provider>
            )}
            {!isLogged && (
                <Layout className="h-screen">
                    <Routes>
                        <Route path="/signin" element={<Signin setLoginState={setLoginState} />} />
                        <Route path="*" element={<Navigate to="/signin" />} />
                    </Routes>
                </Layout>
            )}
        </ConfigProvider>
    );
};

export default App;
