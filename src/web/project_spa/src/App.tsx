import './App.css';
import { Link, Navigate, Route, Routes, useParams } from 'react-router-dom';
import Dashboard from './pages/dashboard';

const App = () => {
    const Comp = () => {
        const params = useParams();
        console.log(params);
        return (
            <>
                <span></span>
            </>
        );
    };
    return (
        <>
            <Link to="/">Home</Link>
            <Link to="/about">About</Link>{' '}
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/project/:projectId" element={<Comp />} />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </>
    );
};

export default App;
