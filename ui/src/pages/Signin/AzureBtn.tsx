import { PublicClientApplication } from '@azure/msal-browser';
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
    // system: {
    //     loggerOptions: {
    //         loggerCallback: (level, message, containsPii) => {
    //             console.log(level);
    //             console.log(message);
    //             console.log(containsPii);
    //             return;
    //         }
    //     }
    // }
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
    return <button onClick={handleClick}>Login by Azure</button>;
};
export default AzureBtn;
