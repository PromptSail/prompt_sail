import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Project from './pages/Project';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Transaction from './pages/Transaction';

const App = () => {
    return (
        <>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/projects/:projectId" element={<Project />} />
                <Route
                    path="/projects/:projectId/transaction/:transactionId"
                    element={<Transaction />}
                />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
            <ToastContainer />
        </>
    );
};

export default App;
