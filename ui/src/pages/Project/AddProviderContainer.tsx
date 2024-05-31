import { CheckSquareOutlined, PlusSquareOutlined } from '@ant-design/icons';
import { Button, Flex, Typography } from 'antd';
import { FormikValuesTemplate } from '../../components/ProjectForms/types';
import { SetStateAction, useState } from 'react';
import Container from '../../components/Container/Container';
import ProviderForm from '../../components/ProjectForms/ProviderDetails/ProviderForm';
import { ItemType } from 'rc-collapse/es/interface';

const { Title } = Typography;

interface Props {
    providers: typeof FormikValuesTemplate.ai_providers;
    slug: string;
    onSubmitSuccess: (values: (typeof FormikValuesTemplate.ai_providers)[number]) => void;
    setProviders: (list: SetStateAction<typeof FormikValuesTemplate.ai_providers>) => void;
    setActiveKeys: (list: SetStateAction<number[]>) => void;
    setItems: (list: SetStateAction<ItemType[]>) => void;
}

const AddProviderContainer: React.FC<Props> = ({
    providers,
    slug,
    onSubmitSuccess,
    setActiveKeys
}) => {
    const [isOpenForm, setOpenForm] = useState(false);
    const [label, setLabel] = useState('');

    return (
        <>
            {!isOpenForm && (
                <Button
                    className="me-auto mb-[12px]"
                    type="dashed"
                    icon={<PlusSquareOutlined />}
                    onClick={() => {
                        setOpenForm(true);
                        setActiveKeys([providers.length]);
                    }}
                >
                    Add{providers.length > 0 ? ' next' : ''} AI Provider
                </Button>
            )}
            {isOpenForm && (
                <Container>
                    <Flex justify="space-between">
                        <Title level={2} className="h5 m-0 lh-0">
                            {label.length > 0 ? label : 'New AI Provider'}
                        </Title>
                        <Button
                            className="my-auto"
                            type="default"
                            size="small"
                            icon={<CheckSquareOutlined />}
                            htmlType="submit"
                            form="projectDetails_addProvider"
                        >
                            Save
                        </Button>
                    </Flex>
                    <ProviderForm
                        slug={slug}
                        onOk={(values) => {
                            onSubmitSuccess(values);
                            setOpenForm(false);
                        }}
                        providers={providers}
                        formId={'projectDetails_addProvider'}
                        handleFormikInstance={(formik) => setLabel(formik.values.deployment_name)}
                    />
                </Container>
            )}
        </>
    );
};
export default AddProviderContainer;
