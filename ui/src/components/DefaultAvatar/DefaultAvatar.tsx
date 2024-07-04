import { UserOutlined } from '@ant-design/icons';

const DefaultAvatar: React.FC<{ circle?: number; icon?: number }> = ({
    circle = 32,
    icon = 20
}) => (
    <div
        className={`w-[${circle}px] h-[${circle}px] bg-Primary/colorPrimary rounded-full relative my-auto`}
    >
        <UserOutlined
            className={`text-white text-[${icon}px] absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-55%]`}
        />
    </div>
);
export default DefaultAvatar;
