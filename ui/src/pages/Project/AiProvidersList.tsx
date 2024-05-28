import { Button, Col, Collapse, Divider, Flex, Row, Typography, theme } from 'antd';
import { getProjectResponse } from '../../api/interfaces';
import { makeUrl, toSlug } from '../../helpers/aiProvider';
import {
    CheckSquareOutlined,
    DeleteOutlined,
    DownOutlined,
    EditOutlined,
    FileAddOutlined,
    SaveOutlined
} from '@ant-design/icons';
import { useEffect, useState } from 'react';
import { CollapsibleType } from 'antd/es/collapse/CollapsePanel';
import { ItemType } from 'rc-collapse/es/interface';
import AddProviderContainer from './AddProviderContainer';
import { FormikValuesTemplate } from '../../components/ProjectForms/types';
import ProviderEditableElement from '../../components/ProjectForms/ProviderDetails/ProvidersEditableElement';
const { Text, Title } = Typography;

import React from 'react';

interface Props {
    list: getProjectResponse['ai_providers'];
    slug: getProjectResponse['slug'];
    onUpdateProviders: (providers: typeof FormikValuesTemplate.ai_providers) => void;
}

const AiProvidersList: React.FC<Props> = ({ list, slug, onUpdateProviders, ...rest }) => {
    const { token } = theme.useToken();
    const [collapseTrigger, setcollapseTrigger] = useState<CollapsibleType>('header');
    const [isEditing, setIsEditing] = useState(false);
    const ItemLabel = (name: string) => (
        <Flex justify="space-between" {...rest}>
            {/* <div key={}></div> */}
            <Title level={2} className="h5 m-0 lh-0">
                {name}
            </Title>
            <Flex gap={12}>
                <Button
                    icon={<EditOutlined />}
                    size="small"
                    type="text"
                    onMouseEnter={() => setcollapseTrigger('icon')}
                    onMouseLeave={() => setcollapseTrigger('header')}
                    onClick={() => {
                        setProviders((prevState) => {
                            const index = prevState.findIndex(
                                (item) => item.deployment_name === name
                            );
                            setItems((prevItems) =>
                                prevItems.map((el, id) =>
                                    id !== index
                                        ? el
                                        : {
                                              ...prevItems[index],
                                              label: (
                                                  <Flex justify="space-between">
                                                      <Title level={2} className="h5 m-0 lh-0">
                                                          {/* {label.length > 0
                                                              ? label
                                                              : 'New AI Provider'} */}
                                                          'test'
                                                      </Title>
                                                      <Button
                                                          className="my-auto"
                                                          type="default"
                                                          size="small"
                                                          icon={<CheckSquareOutlined />}
                                                          htmlType="submit"
                                                          form={`projectDetails_editProvider${index}`}
                                                      >
                                                          Save
                                                      </Button>
                                                  </Flex>
                                              ),
                                              children: (
                                                  <ProviderEditableElement
                                                      initialValues={prevState[index]}
                                                      onSubmit={(values) => {
                                                          setProviders((prevState) => {
                                                              const newList = prevState.map(
                                                                  (el, id) =>
                                                                      id !== index
                                                                          ? el
                                                                          : {
                                                                                ...values,
                                                                                slug: toSlug(
                                                                                    values.deployment_name
                                                                                )
                                                                            }
                                                              );
                                                              setItems(CollapseItems(newList));
                                                              return newList;
                                                          });
                                                      }}
                                                      slugForProxy={slug}
                                                      formId={`projectDetails_editProvider${index}`}
                                                  />
                                              )
                                          }
                                )
                            );
                            return prevState;
                        });
                    }}
                >
                    Edit
                </Button>
                <Button
                    icon={<DeleteOutlined />}
                    size="small"
                    type="text"
                    onMouseEnter={() => setcollapseTrigger('icon')}
                    onMouseLeave={() => setcollapseTrigger('header')}
                    onClick={() => {
                        setProviders((prevState) => {
                            const newList = prevState.filter(
                                (item) => item.deployment_name !== name
                            );
                            setItems(CollapseItems(newList));
                            return newList;
                        });
                    }}
                />
                <Divider type="vertical" className="h-full m-0" />
            </Flex>
        </Flex>
    );
    const [providers, setProviders] = useState(list);
    const CollapseItems = (list: typeof FormikValuesTemplate.ai_providers) =>
        list.map((el, item_id) => ({
            key: item_id,
            label: ItemLabel(el.deployment_name),
            style: {
                background: token.colorBgContainer,
                // @ts-expect-error token.Collapse.colorBorder is correctly defined in /ui/src/theme-light.tsx
                border: `1px solid ${token.Collapse.colorBorder}`,
                borderRadius: '8px'
            },
            onItemClick: () => {
                setActiveKeys((old) =>
                    old.includes(item_id) ? old.filter((key) => key !== item_id) : [...old, item_id]
                );
            },
            children: (
                <Flex vertical gap={16}>
                    <Row gutter={12}>
                        <Col flex="129px" className="text-end">
                            <Text>AI Provider:</Text>
                        </Col>
                        <Col>
                            <Text>{el.provider_name}</Text>
                        </Col>
                    </Row>
                    <Row gutter={12}>
                        <Col flex="129px" className="text-end">
                            <Text className="!m-0">Deployment name:</Text>
                        </Col>
                        <Col>
                            <Text>{el.deployment_name}</Text>
                        </Col>
                    </Row>
                    <Row gutter={12}>
                        <Col flex="129px" className="text-end">
                            <Text>API base URL:</Text>
                        </Col>
                        <Col flex="auto">
                            <Text>{el.api_base}</Text>
                        </Col>
                    </Row>
                    <Row gutter={12}>
                        <Col flex="129px" className="text-end">
                            <Text>Proxy URL:</Text>
                        </Col>
                        <Col flex="auto">
                            <Text>{makeUrl(slug, el.deployment_name)}</Text>
                        </Col>
                    </Row>
                    <Row gutter={12}>
                        <Col flex="129px" className="text-end"></Col>
                        <Col flex="auto">
                            <Button size="small" icon={<FileAddOutlined />}>
                                Proxy URL Configuration
                            </Button>
                        </Col>
                    </Row>
                </Flex>
            )
        }));

    const [items, setItems] = useState<ItemType[]>(CollapseItems(providers));
    const [activeKeys, setActiveKeys] = useState<number[]>(
        items.length < 4 ? items.map((_el, id) => id) : []
    );
    useEffect(() => {
        if (providers !== list) setIsEditing(true);
        else setIsEditing(false);
    }, [providers]);
    return (
        <>
            <Collapse
                collapsible={collapseTrigger}
                activeKey={activeKeys}
                style={{
                    background: token.Layout?.bodyBg,
                    border: 'none',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 12,
                    padding: 0
                }}
                expandIcon={({ isActive }) => (
                    <DownOutlined className="my-auto !text-[14px]" rotate={isActive ? 180 : 0} />
                )}
                onChange={(a) => {
                    console.log(a);
                }}
                expandIconPosition="end"
                items={items}
            />

            <AddProviderContainer
                providers={providers}
                slug={slug}
                setProviders={setProviders}
                setActiveKeys={setActiveKeys}
                setItems={setItems}
                onSubmitSuccess={(values) => {
                    setProviders((prevState) => {
                        const newList = [
                            ...prevState,
                            {
                                ...values,
                                slug: toSlug(values.deployment_name)
                            }
                        ];
                        setItems(CollapseItems(newList));
                        return newList;
                    });
                }}
            />

            {isEditing && (
                <Flex
                    justify="flex-end"
                    gap={16}
                    className="px-[24px] py-[16px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px]"
                >
                    <Button
                        className="my-auto"
                        size="large"
                        type="text"
                        onClick={() => {
                            setProviders(() => {
                                setItems(CollapseItems(list));
                                return list;
                            });
                            setActiveKeys(items.length < 4 ? items.map((_el, id) => id) : []);
                        }}
                    >
                        Cancel
                    </Button>
                    <Button
                        className="my-auto"
                        type="primary"
                        size="large"
                        icon={<SaveOutlined />}
                        htmlType="submit"
                        onClick={() => {
                            onUpdateProviders(providers);
                            setIsEditing(false);
                        }}
                    >
                        Save
                    </Button>
                </Flex>
            )}
        </>
    );
};
export default AiProvidersList;
