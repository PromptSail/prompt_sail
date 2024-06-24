import { CheckSquareOutlined, PlusSquareOutlined } from '@ant-design/icons';
import { Button, Flex, Typography } from 'antd';
import { FormikValuesTemplate } from '../../components/ProjectForms/types';
import { SetStateAction, useState } from 'react';
import Container from '../../components/Container/Container';
import ProviderForm from '../../components/ProjectForms/ProviderDetails/ProviderForm';
import { ItemType } from 'rc-collapse/es/interface';
import noData from '../../assets/box.svg';

const { Title, Paragraph } = Typography;

interface Props {
    providers: typeof FormikValuesTemplate.ai_providers;
    items: ItemType[];
    slug: string;
    onSubmitSuccess: (values: (typeof FormikValuesTemplate.ai_providers)[number]) => void;
    setProviders: (list: SetStateAction<typeof FormikValuesTemplate.ai_providers>) => void;
    setActiveKeys: (list: SetStateAction<number[]>) => void;
    setItems: (list: SetStateAction<ItemType[]>) => void;
}

const AddProviderContainer: React.FC<Props> = ({
    providers,
    items,
    slug,
    onSubmitSuccess,
    setActiveKeys
}) => {
    const [isOpenForm, setOpenForm] = useState(false);
    const [label, setLabel] = useState('');
    const buttonFunc = () => {
        setOpenForm(true);
        const disabledItems = items
            .filter((item) => item.collapsible === 'disabled')
            .map((item) => item.key) as number[];

        setActiveKeys([...disabledItems, providers.length]);
    };

    return (
        <>
            {!isOpenForm && (
                <>
                    {!providers.length ? (
                        <Flex align="center" justify="center" vertical className="my-20">
                            <img src={noData} alt="No Data" width={150} />
                            <Title level={2}>No providers</Title>
                            <Paragraph className="!mt-4">
                                Add first AI Provider to this project
                            </Paragraph>
                            <Button
                                type="primary"
                                icon={<PlusSquareOutlined />}
                                onClick={buttonFunc}
                            >
                                Add AI Provider
                            </Button>
                        </Flex>
                    ) : (
                        <Button
                            className="me-auto mb-[12px]"
                            type="dashed"
                            icon={<PlusSquareOutlined />}
                            onClick={buttonFunc}
                        >
                            Add{providers.length > 0 ? ' next' : ''} AI Provider
                        </Button>
                    )}
                </>
            )}
            {isOpenForm && (
                <Container>
                    <Flex justify="space-between">
                        <Title level={2} className="h5 m-0 lh-0">
                            {label.length > 0 ? label : 'New AI Provider'}
                        </Title>
                    </Flex>
                    <div className="px-[24px] py-[16px] ">
                        <ProviderForm
                            slug={slug}
                            onOk={(values) => {
                                onSubmitSuccess(values);
                                setOpenForm(false);
                            }}
                            providers={providers}
                            formId={'projectDetails_addProvider'}
                            handleFormikInstance={(formik) =>
                                setLabel(formik.values.deployment_name)
                            }
                        />
                        <Flex gap={8}>
                            <Button
                                className="my-auto"
                                onClick={() => {
                                    setOpenForm(false);
                                    const disabledItems = items
                                        .filter((item) => item.collapsible === 'disabled')
                                        .map((item) => item.key) as number[];

                                    setActiveKeys([
                                        ...disabledItems,
                                        ...(providers.length < 4
                                            ? providers.map((_el, id) => id)
                                            : [])
                                    ]);
                                }}
                            >
                                Cancel
                            </Button>
                            <Button
                                className="my-auto"
                                type="primary"
                                icon={<CheckSquareOutlined />}
                                htmlType="submit"
                                form="projectDetails_addProvider"
                            >
                                Save
                            </Button>
                        </Flex>
                    </div>
                </Container>
            )}
        </>
    );
};
export default AddProviderContainer;
