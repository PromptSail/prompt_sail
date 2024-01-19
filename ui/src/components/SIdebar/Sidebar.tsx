import { MutableRefObject, ReactNode, useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router';

interface Props {
    children?: ReactNode;
    classes?: string;
    pageRef: MutableRefObject<null>;
}

const Sidebar: React.FC<Props> = ({ children, classes, pageRef }) => {
    const navigate = useNavigate();
    const [isSidebarHide, toggleSidebar] = useState(false);
    useEffect(() => {
        if (pageRef.current) {
            const page = pageRef.current as HTMLDivElement;
            page.style.setProperty('transition', 'margin 500ms ease');
            page.style.setProperty('margin-left', isSidebarHide ? '100px' : '350px');
        }
    }, [isSidebarHide]);
    return (
        <>
            <div
                style={{ left: isSidebarHide ? -250 : 0, transition: 'left 500ms ease' }}
                className={`sidebar${classes ? ' ' + classes : ''}`}
            >
                <div className="sidebar__container">
                    <div className="menu">
                        <Button variant="primary" className="w-full" onClick={() => navigate('/')}>
                            Projects
                        </Button>
                        <Button
                            variant="primary"
                            className="w-full"
                            onClick={() => navigate('/transactions')}
                        >
                            Transactions
                        </Button>
                        {children}
                    </div>
                </div>
                <div
                    style={{
                        right: isSidebarHide ? -65 : undefined
                    }}
                    className="sidebar__toggleButtonContainer"
                >
                    <Button
                        style={{
                            transform: isSidebarHide ? 'rotate(180deg)' : undefined
                        }}
                        onClick={() => toggleSidebar((v) => !v)}
                        className="toggleButton"
                    >
                        {'<'}
                    </Button>
                </div>
            </div>
        </>
    );
};
export default Sidebar;
