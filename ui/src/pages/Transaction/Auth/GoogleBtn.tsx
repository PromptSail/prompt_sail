import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
const GoogleBtn: React.FC<{ setResponse: (arg: string) => void }> = ({ setResponse }) => {
    return (
        <GoogleLogin
            onSuccess={(credentialResponse) => {
                const decoded = jwtDecode(credentialResponse.credential || '');
                setResponse(
                    JSON.stringify({ response: credentialResponse, decoded: decoded }, null, 4)
                );
            }}
            onError={() => {
                setResponse('login failed');
            }}
        />
    );
};
export default GoogleBtn;
