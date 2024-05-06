import { GoogleLogin } from '@react-oauth/google';

const GoogleBtn: React.FC<{ onOk: (arg: string) => void }> = ({ onOk }) => {
    return (
        <GoogleLogin
            onSuccess={(credentialResponse) => {
                onOk(credentialResponse.credential || '');
            }}
            onError={() => {
                console.error('Google - login failed');
            }}
        />
    );
};
export default GoogleBtn;
