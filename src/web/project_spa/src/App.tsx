import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Project from './pages/Project';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
    return (
        <>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/project/:projectId" element={<Project />} />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
            <ToastContainer />
        </>
    );
};

export default App;
