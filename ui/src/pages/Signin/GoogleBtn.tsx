import { GoogleLogin } from '@react-oauth/google';

const GoogleBtn: React.FC<{ onOk: (arg: string) => void; width: number }> = ({ onOk, width }) => {
    return (
        <GoogleLogin
            onSuccess={(credentialResponse) => {
                onOk(credentialResponse.credential || '');
            }}
            onError={() => console.error('Google - login failed')}
            width={width}
            theme="filled_blue"
        />
    );
};
export default GoogleBtn;
