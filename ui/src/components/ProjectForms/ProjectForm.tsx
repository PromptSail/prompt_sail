import { FormikProps, useFormik } from 'formik';
import { useState } from 'react';
import { projectSchema } from '../../api/formSchemas';
import { toSlug } from '../../helpers/aiProvider';
import { Button, Flex, Steps } from 'antd';
import { FormikValuesTemplate } from './types';
import ProjectDetails from './ProjectDetails';
import ProviderDetails from './ProviderDetails/ProviderDetails';
import { CheckSquareOutlined, RightSquareOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { getStorageOrganization } from '../../storage/organization';

interface Props {
    submitFunc: (values: typeof FormikValuesTemplate) => Promise<void>;
    formId: string;
    projectId?: string;
}

const ProjectForm: React.FC<Props> = ({ submitFunc }) => {
    const navigate = useNavigate();
    const [stepsCurrent, setStepsCurrent] = useState(0);
    const [project, setProject] = useState<typeof FormikValuesTemplate>({
        ...FormikValuesTemplate,
        ai_providers: [] as typeof FormikValuesTemplate.ai_providers
    });
    const formikDetails = useFormik({
        initialValues: { ...project, skip: false },
        onSubmit: async (values) => {
            const valuesAndOrg = {
                ...values,
                org_id: getStorageOrganization()?.id || ''
            };
            setProject((old) => ({
                ...valuesAndOrg,
                slug: toSlug(values.slug),
                ai_providers: old.ai_providers
            }));
            if (valuesAndOrg.skip) {
                submitFunc(valuesAndOrg);
            } else setStepsCurrent(1);
        },
        validationSchema: projectSchema,
        validateOnChange: false
    });
    return (
        <Flex gap={12} className="px-[24px] max-w-[1600px] w-full mx-auto" vertical>
            <div className="px-[24px] py-[16px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px]">
                <Steps
                    current={stepsCurrent}
                    className="max-w-[60%]"
                    items={[
                        {
                            title: 'Project details'
                        },
                        {
                            title: 'Provider details'
                        }
                    ]}
                />
            </div>
            <Flex vertical gap={12} className={stepsCurrent === 0 ? '' : 'hidden'}>
                <ProjectDetails
                    formik={formikDetails as unknown as FormikProps<typeof FormikValuesTemplate>}
                />
                <Flex
                    justify="flex-end"
                    gap={16}
                    className="px-[24px] py-[16px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px]"
                >
                    <Button
                        className="my-auto"
                        size="large"
                        type="text"
                        onClick={() => navigate('/')}
                    >
                        Cancel
                    </Button>
                    <Button
                        className="my-auto"
                        size="large"
                        htmlType="submit"
                        form="projectForm_details"
                        onClick={() => {
                            formikDetails.setValues((old) => ({ ...old, skip: true }));
                        }}
                    >
                        Skip second step and create project
                    </Button>
                    <Button
                        className="my-auto"
                        type="primary"
                        size="large"
                        icon={<RightSquareOutlined />}
                        htmlType="submit"
                        form="projectForm_details"
                    >
                        Continue
                    </Button>
                </Flex>
            </Flex>
            <div className={stepsCurrent === 1 ? '' : 'hidden'}>
                <ProviderDetails projectDetails={project} setProjectDetails={setProject} />
                <Flex
                    justify="flex-end"
                    gap={16}
                    className="px-[24px] py-[16px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px]"
                >
                    <Button
                        className="my-auto"
                        size="large"
                        type="text"
                        onClick={() => navigate('/')}
                    >
                        Cancel
                    </Button>
                    <Button
                        className="my-auto"
                        type="default"
                        size="large"
                        onClick={() => setStepsCurrent(0)}
                    >
                        Back
                    </Button>
                    <Button
                        className="my-auto"
                        type="primary"
                        size="large"
                        icon={<CheckSquareOutlined />}
                        htmlType="submit"
                        form="projectForm_providers"
                        onClick={() => {
                            submitFunc(project);
                        }}
                    >
                        Create project
                    </Button>
                </Flex>
            </div>
        </Flex>
    );
};

export default ProjectForm;
