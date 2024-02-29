import { MutableRefObject, ReactNode, SetStateAction, useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { ReactSVG } from 'react-svg';
import Icon from '../../assets/icons/box-arrow-left.svg';
import { checkLogin } from '../../storage/login';

interface Props {
    children?: ReactNode;
    classes?: string;
    pageRef: MutableRefObject<null>;
    setLoginState: (arg: SetStateAction<boolean>) => void;
}

const Sidebar: React.FC<Props> = ({ children, classes, pageRef, setLoginState }) => {
    const navigate = useNavigate();
    const [isSidebarHide, toggleSidebar] = useState(false);
    const user = {
        name: 'John Doe',
        email: 'JohnDoe@gmail.com'
    };
    useEffect(() => {
        if (pageRef.current) {
            const page = pageRef.current as HTMLDivElement;
            page.style.setProperty('transition', 'margin 500ms ease');
            page.style.setProperty('margin-left', isSidebarHide ? '0' : '250px');
        }
    }, [isSidebarHide]);

    return (
        <>
            <div
                style={{ left: isSidebarHide ? -250 : 0, transition: 'left 500ms ease' }}
                className={`sidebar${classes ? ' ' + classes : ''}`}
            >
                <div className="sidebar__container">
                    <div className="sidebar-top">
                        <div className="user">
                            <p className="user__name">{user.name}</p>
                            <p className="user__email">{user.email}</p>
                        </div>
                        <div className="menu">
                            <button className="w-full" onClick={() => navigate('/')}>
                                Projects
                            </button>
                            <button className="w-full" onClick={() => navigate('/transactions')}>
                                Transactions
                            </button>
                            {children}
                        </div>
                    </div>
                    <div className="sidebar-bottom">
                        <button
                            className="outline-none"
                            onClick={() => {
                                localStorage.removeItem('login');
                                setLoginState(checkLogin());
                            }}
                        >
                            <div>
                                <ReactSVG src={Icon} />
                            </div>
                            <span>Log out</span>
                        </button>
                    </div>
                </div>
                <div
                    style={{
                        right: isSidebarHide ? -65 : undefined
                    }}
                    className="sidebar__toggleButtonContainer"
                >
                    <button
                        style={{
                            transform: isSidebarHide ? 'rotate(180deg)' : undefined
                        }}
                        onClick={() => toggleSidebar((v) => !v)}
                        className="toggleButton"
                    >
                        {'<'}
                    </button>
                </div>
            </div>
        </>
    );
};
export default Sidebar;
