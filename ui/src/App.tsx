import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard/Dashboard';
import Project from './pages/Project/Project';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Transactions from './pages/Transactions';
import Sidebar from './components/Sidebar/Sidebar';

import { useState } from 'react';
import Signin from './pages/Signin';
import { checkLogin } from './storage/login';
import { Layout } from 'antd';
import Transaction from './pages/Transaction/Transaction';

const App = () => {
    const [isLogged, setLoginState] = useState(checkLogin());
    if (isLogged) {
        return (
            <>
                <Layout className="h-screen">
                    <Sidebar setLoginState={setLoginState} />
                    <Layout style={{ marginLeft: '250px', padding: '0 50px' }}>
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
                <ToastContainer />
            </>
        );
    } else
        return (
            <Layout className="h-screen">
                <Routes>
                    <Route path="/signin" element={<Signin setLoginState={setLoginState} />} />
                    <Route path="*" element={<Navigate to="/signin" />} />
                </Routes>
            </Layout>
        );
};

export default App;
