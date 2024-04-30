import { config } from './config';
import { PublicClientApplication } from '@azure/msal-browser';
const msalInstance = new PublicClientApplication({
    auth: {
        clientId: config.azure.clientId,
        redirectUri: config.azure.redirectUrl,
        authority: config.azure.authority
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
const AzureBtn: React.FC<{ setResponse: (arg: string) => void }> = ({ setResponse }) => {
    const handleClick = async () => {
        // console.log(msalInstance)
        try {
            // const url = `https://login.microsoftonline.com/${config.azure.tenant}/oauth2/v2.0/authorize?client_id=${config.azure.clientId}&response_type=code&redirect_uri=${config.azure.redirectUrl}&response_mode=query&scope=https://graph.microsoft.com/mail.read`
            // console.log(url)
            // const response  = await fetch(url)
            await msalInstance.initialize();
            await msalInstance.loginPopup({
                scopes: config.azure.scopes,
                prompt: 'select_account'
            });
            console.log(msalInstance.getAllAccounts());
            setResponse(JSON.stringify({ response: msalInstance.getAllAccounts()[0] }, null, 4));
            // console.log(response)
        } catch (error) {
            console.error(error);
            setResponse(JSON.stringify({ response: 'Login failed' }, null, 4));
        }
    };
    return <button onClick={handleClick}>Login by Azure</button>;
};
export default AzureBtn;
