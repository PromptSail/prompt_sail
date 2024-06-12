import { WindowsFilled } from '@ant-design/icons';
import { PublicClientApplication } from '@azure/msal-browser';
import { Button } from 'antd';
const { CLIENT_ID, SCOPES, AUTHORITY } = SSO_AZURE;
const msalInstance = new PublicClientApplication({
    auth: {
        clientId: CLIENT_ID,
        redirectUri: window.location.href,
        authority: AUTHORITY
    },
    cache: {
        cacheLocation: 'sessionStorage',
        storeAuthStateInCookie: true
    }
});
const AzureBtn: React.FC<{ onOk: (arg: string) => void }> = ({ onOk }) => {
    const handleClick = async () => {
        try {
            await msalInstance.initialize();
            await msalInstance.loginPopup({
                scopes: SCOPES,
                prompt: 'select_account'
            });
            onOk(msalInstance.getAllAccounts()[0].idToken || '');
        } catch (error) {
            console.error('Azure - login failed');
            console.error(error);
        }
    };
    return (
        <Button
            type="primary"
            size="large"
            className="w-full"
            icon={<WindowsFilled />}
            onClick={handleClick}
        >
            Login by Azure
        </Button>
    );
};
export default AzureBtn;
