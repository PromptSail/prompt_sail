import { UserOutlined } from '@ant-design/icons';

const DefaultAvatar: React.FC = () => (
    <div className="w-[32px] h-[32px] bg-Primary/colorPrimary rounded-full relative my-auto">
        <UserOutlined className="text-white text-[20px] absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-55%]" />
    </div>
);
export default DefaultAvatar;
