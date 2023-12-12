import { ReactNode } from 'react';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router';

interface Props {
    children?: ReactNode;
    classes?: string;
}

const Sidebar: React.FC<Props> = ({ children, classes }) => {
    const navigate = useNavigate();
    return (
        <>
            <div className={classes}>
                <Button variant="primary" className="w-full" onClick={() => navigate('/')}>
                    Projects
                </Button>
                {children}
            </div>
        </>
    );
};
export default Sidebar;
