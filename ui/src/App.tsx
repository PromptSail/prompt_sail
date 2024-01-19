import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Project from './pages/Project';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Transaction from './pages/Transaction';
import Sidebar from './components/Sidebar/Sidebar';
import AllTransactions from './pages/AllTransactions';
import { useRef } from 'react';

const App = () => {
    const page = useRef(null);
    return (
        <>
            <div className="h-screen">
                <Sidebar pageRef={page}></Sidebar>
                <div
                    ref={page}
                    style={{ marginLeft: '350px' }}
                    className="overflow-y-auto mx-[100px]"
                >
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/projects/:projectId" element={<Project />} />
                        <Route path="/transactions" element={<AllTransactions />} />
                        <Route path="/transactions/:transactionId" element={<Transaction />} />
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </div>
            </div>
            <ToastContainer />
        </>
    );
};

export default App;
