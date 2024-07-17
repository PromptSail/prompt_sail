import { Button, Col, Collapse, Divider, Flex, Input, Row, Select, Typography, theme } from 'antd';
import { getProjectResponse } from '../../api/interfaces';
import { makeUrl, toSlug } from '../../helpers/aiProvider';
import {
    CheckSquareOutlined,
    CopyOutlined,
    DeleteOutlined,
    DownOutlined,
    EditOutlined,
    FileAddOutlined
} from '@ant-design/icons';
import { isValidElement, useContext, useEffect, useState } from 'react';
import { Context } from '../../context/Context';
import { CollapsibleType } from 'antd/es/collapse/CollapsePanel';
import { ItemType } from 'rc-collapse/es/interface';
import AddProviderContainer from './AddProviderContainer';
import { FormikValuesTemplate } from '../../components/ProjectForms/types';
import ProviderEditableElement from '../../components/ProjectForms/ProviderDetails/ProvidersEditableElement';
import { useGetModels } from '../../api/queries';
const { Text, Title, Paragraph } = Typography;

interface Props {
    list: getProjectResponse['ai_providers'];
    slug: getProjectResponse['slug'];
    onUpdateProviders: (providers: typeof FormikValuesTemplate.ai_providers) => void;
}

const AiProvidersList: React.FC<Props> = ({ list, slug, onUpdateProviders, ...rest }) => {
    const { token } = theme.useToken();
    const { modal } = useContext(Context);
    const [collapseTrigger, setcollapseTrigger] = useState<CollapsibleType>('header');
    const ItemLabel = (name: string) => (
        <Flex justify="space-between" {...rest}>
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
                            const cancelItem = items[index];
                            setItems((prevItems) => {
                                const newItems = prevState.map((el, id) =>
                                    id !== index
                                        ? prevItems[id]
                                        : {
                                              ...prevItems[index],
                                              collapsible: 'disabled' as CollapsibleType,
                                              label: (
                                                  <Flex justify="space-between">
                                                      <Title level={2} className="h5 m-0 lh-0">
                                                          {el.deployment_name}
                                                      </Title>
                                                  </Flex>
                                              ),
                                              children: (
                                                  <>
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
                                                                  setItems((prevItems) =>
                                                                      newList.map((el, id) =>
                                                                          id === index
                                                                              ? CollapseItem(el, id)
                                                                              : prevItems[id]
                                                                      )
                                                                  );
                                                                  onUpdateProviders(newList);
                                                                  return newList;
                                                              });
                                                          }}
                                                          showSubmitButton={false}
                                                          slugForProxy={slug}
                                                          formId={`projectDetails_editProvider${index}`}
                                                      />{' '}
                                                      <Flex gap={8}>
                                                          <Button
                                                              className="my-auto"
                                                              onClick={() => {
                                                                  setItems((innerPrevItems) =>
                                                                      innerPrevItems.map((el, id) =>
                                                                          id !== index
                                                                              ? el
                                                                              : cancelItem
                                                                      )
                                                                  );
                                                              }}
                                                          >
                                                              Cancel
                                                          </Button>
                                                          <Button
                                                              className="my-auto"
                                                              type="primary"
                                                              icon={<CheckSquareOutlined />}
                                                              htmlType="submit"
                                                              form={`projectDetails_editProvider${index}`}
                                                          >
                                                              Save
                                                          </Button>
                                                      </Flex>
                                                  </>
                                              )
                                          }
                                );
                                setActiveKeys(
                                    newItems
                                        .filter((el) => el.collapsible === 'disabled')
                                        .map((el) => el.key as number)
                                );
                                return newItems;
                            });
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
                        if (modal)
                            modal.confirm({
                                title: 'Delete AI Provider',
                                icon: <></>,
                                content: (
                                    <>
                                        <Paragraph className="!m-0">
                                            Are you sure you want to delete "{name}" AI Provider?
                                        </Paragraph>
                                        <Paragraph className="!m-0">
                                            You will loose all your data.
                                        </Paragraph>
                                    </>
                                ),
                                onOk() {
                                    const newList = providers.filter(
                                        (el) => el.deployment_name !== name
                                    );
                                    setProviders(newList);
                                    onUpdateProviders(newList);
                                    setItems((prevItems) =>
                                        prevItems.filter((el) => {
                                            const childrenProps = isValidElement(el.children)
                                                ? el.children.props
                                                : {};
                                            return childrenProps.el?.deployment_name !== name;
                                        })
                                    );
                                },
                                okButtonProps: {
                                    danger: true,
                                    icon: <DeleteOutlined />
                                },
                                okText: 'Delete',
                                closable: true
                            });
                    }}
                />
                <Divider type="vertical" className="h-full m-0" />
            </Flex>
        </Flex>
    );
    const [providers, setProviders] = useState(list);
    const CollapseItem = (
        elem: (typeof FormikValuesTemplate.ai_providers)[number],
        id: number
    ): ItemType => ({
        key: id,
        label: ItemLabel(elem.deployment_name),
        style: {
            background: token.colorBgContainer,
            // @ts-expect-error token.Collapse.colorBorder is correctly defined in /ui/src/theme-light.tsx
            border: `1px solid ${token.Collapse.colorBorder}`,
            borderRadius: '8px'
        },
        onItemClick: () => {
            setActiveKeys((old) =>
                old.includes(id) ? old.filter((key) => key !== id) : [...old, id]
            );
        },
        children: <ProviderDescription el={elem} slug={slug} />
    });

    const [items, setItems] = useState<ItemType[]>(providers.map((el, id) => CollapseItem(el, id)));
    const [activeKeys, setActiveKeys] = useState<number[]>(
        items.length < 4 ? items.map((_el, id) => id) : []
    );
    return (
        <>
            {!!providers.length && (
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
                        <DownOutlined
                            className="my-auto !text-[14px]"
                            rotate={isActive ? 180 : 0}
                        />
                    )}
                    expandIconPosition="end"
                    items={items}
                />
            )}
            <AddProviderContainer
                providers={providers}
                items={items}
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
                        setItems((prevItems) => [
                            ...prevItems,
                            CollapseItem(
                                {
                                    ...values,
                                    slug: toSlug(values.deployment_name)
                                },
                                prevItems.length
                            )
                        ]);
                        onUpdateProviders(newList);
                        return newList;
                    });
                }}
            />
        </>
    );
};

const ProviderDescription: React.FC<{
    el: (typeof FormikValuesTemplate.ai_providers)[number];
    slug: string;
}> = ({ el, slug }) => {
    const [isOpenProxyConf, setOpenProxyConf] = useState(false);
    const [AllTags, setAllTags] = useState<string>('');
    const [Tags, setTags] = useState<string>('');
    const [AIModelVersionTag, setAIModelVersionTag] = useState<string>('');
    const priceList = useGetModels();
    useEffect(() => {
        const model = (Tags.length ? `&` : '?') + AIModelVersionTag;
        const alltags = Tags + (AIModelVersionTag.length ? model : '');
        setAllTags(alltags + (alltags.length ? '&' : '?') + 'target_path=');
    }, [Tags, AIModelVersionTag]);
    return (
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
                    <Text copyable>{makeUrl(slug, el.slug)}</Text>
                </Col>
            </Row>
            <Row gutter={12}>
                <Col flex="129px" className="text-end"></Col>
                <Col flex="auto">
                    {!isOpenProxyConf && (
                        <Button
                            size="small"
                            icon={<FileAddOutlined />}
                            onClick={() => setOpenProxyConf(true)}
                        >
                            Proxy URL Configuration
                        </Button>
                    )}
                    {isOpenProxyConf && (
                        <Flex
                            className="bg-Fill/colorFillTertiary p-[12px] rounded-[4px]"
                            gap={16}
                            vertical
                        >
                            <Text>
                                This generator/configurator/builder allows you to easily add tags to
                                proxy URL
                            </Text>
                            <div>
                                <Paragraph className="!m-0 text-Text/colorText">
                                    General Tags:
                                </Paragraph>
                                <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                                    Enter the tags you want to pass via Proxy URL
                                </Paragraph>
                                <Select
                                    mode="tags"
                                    className="max-w-[50%] w-full"
                                    placeholder="General Tags"
                                    dropdownStyle={{ display: 'none' }}
                                    allowClear
                                    suffixIcon={<></>}
                                    onChange={(value: string[]) => {
                                        setTags(value.length > 0 ? '?tags=' + value.join(',') : '');
                                    }}
                                />
                            </div>
                            {el.provider_name.toLowerCase().includes('azure') && (
                                <div>
                                    <Paragraph className="!m-0 text-Text/colorText">
                                        AI Model Name and Version Tag:
                                    </Paragraph>
                                    <Paragraph className="!mb-[8px] text-Text/colorTextDescription">
                                        Specifying the model name and version is only necessary for
                                        Azure deployments - it will allow calculate cost properly.
                                    </Paragraph>
                                    <Select
                                        showSearch
                                        className="max-w-[50%] w-full"
                                        placeholder="AI Model Name and Version Tag"
                                        loading={priceList.isLoading}
                                        options={(() => {
                                            if (priceList.isSuccess) {
                                                return priceList.data
                                                    .filter((el) =>
                                                        el.provider.toLowerCase().includes('azure')
                                                    )
                                                    .map((el) => ({
                                                        label: el.model_name,
                                                        value: el.model_name
                                                    }));
                                            } else return [{ label: 'loading', value: 'loading' }];
                                        })()}
                                        onChange={(value) => {
                                            setAIModelVersionTag(
                                                value.length > 0 ? 'ai_model_version=' + value : ''
                                            );
                                        }}
                                    />
                                </div>
                            )}
                            <div>
                                <Paragraph className="!m-0 text-Text/colorText">
                                    Proxy URL:
                                </Paragraph>
                                <Flex gap={16}>
                                    <Input
                                        className="max-w-[50%] w-full"
                                        value={makeUrl(slug, el.slug) + AllTags}
                                        disabled
                                    />
                                    <Button
                                        type="primary"
                                        icon={<CopyOutlined />}
                                        onClick={() => {
                                            navigator.clipboard.writeText(
                                                makeUrl(slug, el.slug) + AllTags
                                            );
                                        }}
                                    />
                                </Flex>
                            </div>
                            <Button onClick={() => setOpenProxyConf(false)} className="w-fit">
                                Cancel
                            </Button>
                        </Flex>
                    )}
                </Col>
            </Row>
        </Flex>
    );
};
export default AiProvidersList;
