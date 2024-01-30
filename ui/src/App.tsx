import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Project from './pages/Project';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Transaction from './pages/Transaction';
import Sidebar from './components/Sidebar/Sidebar';
import AllTransactions from './pages/AllTransactions';
import { useRef, useState } from 'react';
import Signin from './pages/Signin';
import { checkLogin } from './storage/login';

const App = () => {
    const page = useRef(null);
    const [isLogged, setLoginState] = useState(checkLogin());
    if (isLogged) {
        return (
            <>
                <div className="h-screen">
                    <Sidebar pageRef={page} setLoginState={setLoginState}></Sidebar>
                    <div ref={page} style={{ marginLeft: '250px' }}>
                        <div
                            style={{ margin: '0 auto', padding: '0 50px' }}
                            className="overflow-y-auto max-w-[1200px]"
                        >
                            <Routes>
                                <Route path="/" element={<Dashboard />} />
                                <Route
                                    path="/projects/:projectId/update"
                                    element={<Project.Update />}
                                />
                                <Route path="/projects/:projectId" element={<Project />} />
                                <Route path="/projects/add" element={<Project.Add />} />
                                <Route path="/transactions" element={<AllTransactions />} />
                                <Route
                                    path="/transactions/:transactionId"
                                    element={<Transaction />}
                                />
                                {/* <Route path="*" element={<Navigate to="/" />} /> */}
                            </Routes>
                        </div>
                    </div>
                </div>
                <ToastContainer />
            </>
        );
    } else
        return (
            <>
                <Routes>
                    <Route path="/signin" element={<Signin setLoginState={setLoginState} />} />
                    <Route path="*" element={<Navigate to="/signin" />} />
                </Routes>
            </>
        );
};

export default App;
