import { HookAPI } from 'antd/es/modal/useModal';
import { NotificationInstance } from 'antd/es/notification/interface';
import { createContext } from 'react';

export const Context = createContext<{
    notification: NotificationInstance | null;
    modal: HookAPI | null;
}>({ notification: null, modal: null });
