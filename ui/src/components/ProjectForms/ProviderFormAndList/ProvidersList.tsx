import { Button, Collapse, Descriptions, Space, Typography } from 'antd';
import { FormikValues } from '../types';
import { makeUrl } from '../../../helpers/aiProvider';
import { SetStateAction } from 'react';
import ProviderForm from './ProviderForm';
const { Paragraph } = Typography;

interface Props {
    ProvidersList: typeof FormikValues.ai_providers;
    projectSlug: string;
    EditedProvider: number | null;
    setEditedProvider: (arg: SetStateAction<number | null>) => void;
    setProvidersList: (list: typeof FormikValues.ai_providers) => void;
    setFormShow: (arg: SetStateAction<boolean>) => void;
}

const ProvidersListCollapse: React.FC<Props> = ({
    ProvidersList,
    projectSlug,
    EditedProvider,
    setEditedProvider,
    setProvidersList,
    setFormShow
}) => {
    return (
        <>
            <Collapse
                accordion
                items={ProvidersList.map((el, id) => ({
                    key: id,
                    label: (
                        <Space size={'large'}>
                            <span>{el.deployment_name}</span>
                            <Paragraph copyable className="!m-0">
                                {makeUrl(projectSlug, el.deployment_name)}
                            </Paragraph>
                        </Space>
                    ),
                    children: (
                        <>
                            <Descriptions
                                column={2}
                                items={[
                                    {
                                        label: 'Provider',
                                        children: el.provider_name,
                                        span: 2
                                    },
                                    {
                                        label: 'Api base',
                                        children: el.api_base,
                                        span: 2
                                    }
                                ]}
                            />
                            <Space className="w-full" styles={{ item: { flex: '1' } }}>
                                <Button
                                    ghost
                                    block
                                    type="primary"
                                    onClick={() => {
                                        if (EditedProvider != id) {
                                            setEditedProvider(id);
                                        } else setEditedProvider(null);
                                    }}
                                >
                                    {`${EditedProvider != id ? '' : 'Cancel '}Edit`}
                                </Button>
                                <Button
                                    danger
                                    block
                                    onClick={() => {
                                        const newList = ProvidersList.filter(
                                            (_el, idx) => idx != id
                                        );
                                        setProvidersList(newList);
                                        if (newList.length < 1) {
                                            setFormShow(true);
                                        }
                                    }}
                                >
                                    Delete
                                </Button>
                            </Space>
                            {EditedProvider == id && (
                                <ProviderForm
                                    EditedProvider={EditedProvider}
                                    ProvidersList={ProvidersList}
                                    setProvidersList={setProvidersList}
                                    setEditedProvider={setEditedProvider}
                                    slug={projectSlug}
                                    setFormShow={setFormShow}
                                />
                            )}
                        </>
                    )
                }))}
            />
        </>
    );
};

export default ProvidersListCollapse;
