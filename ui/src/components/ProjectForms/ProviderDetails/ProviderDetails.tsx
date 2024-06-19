import { Button, Collapse, CollapseProps, Divider, Flex, Typography, theme } from 'antd';
import { FormikValuesTemplate } from '../types';
import { SetStateAction, useContext, useState } from 'react';
import { toSlug } from '../../../helpers/aiProvider';
import { DeleteOutlined, DownOutlined, PlusSquareOutlined } from '@ant-design/icons';
import ProviderEditableElement from './ProvidersEditableElement';
import { CollapsibleType } from 'antd/es/collapse/CollapsePanel';
import ProviderForm from './ProviderForm';
import Container from '../../Container/Container';
import { Context } from '../../../context/Context';

const { Title, Paragraph } = Typography;

interface Props {
    projectDetails: typeof FormikValuesTemplate;
    setProjectDetails: (args: SetStateAction<typeof FormikValuesTemplate>) => void;
}

const ProviderDetails: React.FC<Props> = ({ setProjectDetails, projectDetails }) => {
    const { token } = theme.useToken();
    const { modal } = useContext(Context);
    const [newFormOpened, setNewFormOpened] = useState(true);
    const [collapseTrigger, setcollapseTrigger] = useState<CollapsibleType>('header');
    const items: CollapseProps['items'] = projectDetails.ai_providers.map((el, item_id) => ({
        key: item_id,
        label: (
            <Flex justify="space-between">
                <Title level={2} className="h5 m-0 lh-0">
                    {el.deployment_name}
                </Title>
                <Flex gap={12}>
                    <Button
                        icon={<DeleteOutlined />}
                        size="small"
                        onClick={() => {
                            if (modal)
                                modal.confirm({
                                    title: 'Delete AI Provider',
                                    icon: <></>,
                                    content: (
                                        <>
                                            <Paragraph className="!m-0">
                                                Are you sure you want to delete "
                                                {el.deployment_name}" AI Provider?
                                            </Paragraph>
                                            <Paragraph className="!m-0">
                                                You will loose all your data.
                                            </Paragraph>
                                        </>
                                    ),
                                    onOk() {
                                        const newAiProviders = projectDetails.ai_providers.filter(
                                            (_el, id) => id !== item_id
                                        );
                                        setProjectDetails((old) => ({
                                            ...old,
                                            ai_providers: newAiProviders
                                        }));
                                    },
                                    okButtonProps: {
                                        danger: true,
                                        icon: <DeleteOutlined />
                                    },
                                    okText: 'Delete',
                                    closable: true
                                });
                        }}
                        type="text"
                        onMouseEnter={() => setcollapseTrigger('icon')}
                        onMouseLeave={() => setcollapseTrigger('header')}
                    />
                    <Divider type="vertical" className="h-full m-0" />
                </Flex>
            </Flex>
        ),
        style: {
            background: token.colorBgContainer,
            // @ts-expect-error token.Collapse.colorBorder is correctly defined in /ui/src/theme-light.tsx
            border: `1px solid ${token.Collapse.colorBorder}`,
            borderRadius: '8px'
        },
        children: (
            <ProviderEditableElement
                initialValues={el}
                onSubmit={(values) =>
                    setProjectDetails((old) => {
                        const newAiProviders = old.ai_providers.map((el, id) => {
                            if (id === item_id)
                                return { ...values, slug: toSlug(values.deployment_name) };
                            else return el;
                        });
                        return {
                            ...old,
                            ai_providers: newAiProviders
                        };
                    })
                }
                slugForProxy={projectDetails.slug}
                formId={'projectForm_providerEdit' + item_id}
            />
        )
    }));
    return (
        <Flex gap={12} vertical>
            {projectDetails.ai_providers.length > 0 && (
                <Collapse
                    accordion
                    collapsible={collapseTrigger}
                    defaultActiveKey={[]}
                    style={{
                        background: token.Layout?.bodyBg,
                        border: 'none',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 12,
                        padding: 0
                    }}
                    expandIcon={({ isActive }) => (
                        <DownOutlined
                            className="my-auto !text-[14px]"
                            rotate={isActive ? 180 : 0}
                        />
                    )}
                    expandIconPosition="end"
                    items={items}
                />
            )}
            {newFormOpened && (
                <Container>
                    <Title level={2} className="h5 m-0 pt-0 px-[24px] py-[16px]">
                        Project details
                    </Title>
                    <div>
                        <ProviderForm
                            onOk={(values) => {
                                setProjectDetails((old) => ({
                                    ...old,
                                    ai_providers: [
                                        ...old.ai_providers,
                                        { ...values, slug: toSlug(values.deployment_name) }
                                    ]
                                }));
                                setNewFormOpened(false);
                            }}
                            providers={projectDetails.ai_providers}
                            slug={projectDetails.slug}
                            formId="projectForm_providerAdd"
                        />
                        <Button
                            className="my-auto"
                            type="primary"
                            //   icon={<CheckSquareOutlined />}
                            htmlType="submit"
                            form="projectForm_providerAdd"
                        >
                            Save
                        </Button>
                    </div>
                </Container>
            )}
            <Button
                className="me-auto mb-[12px]"
                type="dashed"
                icon={<PlusSquareOutlined />}
                htmlType="submit"
                onClick={() => setNewFormOpened(true)}
                disabled={newFormOpened}
            >
                Add next AI Provider
            </Button>
        </Flex>
    );
};
export default ProviderDetails;
