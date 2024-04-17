import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard/Dashboard';
import Project from './pages/Project/Project';
import Transactions from './pages/Transactions';
import Sidebar from './components/Sidebar/Sidebar';

import { useState } from 'react';
import Signin from './pages/Signin';
import { checkLogin } from './storage/login';
import { ConfigProvider, Layout } from 'antd';
import Transaction from './pages/Transaction/Transaction';
import theme from './theme-light';

const App = () => {
    const [isLogged, setLoginState] = useState(checkLogin());
    return (
        <ConfigProvider theme={theme}>
            {isLogged && (
                <Layout>
                    <Sidebar setLoginState={setLoginState} />
                    <Layout className="px-[50px] h-screen overflow-auto">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route
                                path="/projects/:projectId/update"
                                element={<Project.Update />}
                            />
                            <Route path="/projects/:projectId" element={<Project />} />
                            <Route path="/projects/add" element={<Project.Add />} />
                            <Route path="/transactions" element={<Transactions />} />
                            <Route path="/transactions/:transactionId" element={<Transaction />} />
                            <Route path="*" element={<Navigate to="/" />} />
                        </Routes>
                    </Layout>
                </Layout>
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
