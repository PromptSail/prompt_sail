import { HookAPI } from 'antd/es/modal/useModal';
import { NotificationInstance } from 'antd/es/notification/interface';
import { createContext } from 'react';
import { getConfig } from '../api/interfaces';

export const Context = createContext<{
    notification: NotificationInstance | null;
    modal: HookAPI | null;
    config: getConfig | null;
}>({ notification: null, modal: null, config: null });
