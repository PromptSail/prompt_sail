import { GoogleCircleFilled } from '@ant-design/icons';
import { useGoogleLogin } from '@react-oauth/google';
import { Button } from 'antd';

const GoogleBtn: React.FC<{ onOk: (arg: string) => void }> = ({ onOk }) => {
    const login = useGoogleLogin({
        onSuccess: (tokenResponse) => {
            onOk(tokenResponse.access_token || '');
        },
        onError: () => {
            console.error('Google - login failed');
        }
    });
    return (
        <Button
            icon={<GoogleCircleFilled />}
            type="primary"
            size="large"
            className="w-full mt-3"
            onClick={() => login()}
        >
            Login by Google
        </Button>
    );
};
export default GoogleBtn;
