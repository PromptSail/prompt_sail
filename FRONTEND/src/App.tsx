import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Project from './pages/Project';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Transaction from './pages/Transaction';
import Sidebar from './components/SIdebar/Sidebar';

const App = () => {
    return (
        <>
            <div className="flex flex-row h-screen overflow-hidden">
                <Sidebar classes="h-full w-full flex-1 bg-zinc-800 p-5 text-light"></Sidebar>
                <div className="flex-[4] overflow-y-auto">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/projects/:projectId" element={<Project />} />
                        <Route path="/transaction/:transactionId" element={<Transaction />} />
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </div>
            </div>
            <ToastContainer />
        </>
    );
};

export default App;
