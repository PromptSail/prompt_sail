import { useGetProject, useUpdateProject } from '../../../api/queries';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Breadcrumb, Button, Flex, Spin, Typography } from 'antd';
import { FormikValuesTemplate } from '../../../components/ProjectForms/types';
import HeaderContainer from '../../../components/HeaderContainer/HeaderContainer';
import { useFormik } from 'formik';
import { projectSchema } from '../../../api/formSchemas';
import ProjectDetails from '../../../components/ProjectForms/ProjectDetails';
import { useContext, useEffect } from 'react';
import { SaveOutlined } from '@ant-design/icons';
import { Context } from '../../../context/Context';

const { Title } = Typography;

const UpdateProject: React.FC = () => {
    const { notification } = useContext(Context);
    const updateProject = useUpdateProject();
    const projectId = useParams().projectId || '';
    const project = useGetProject(projectId);
    const navigate = useNavigate();
    const submit = async (values: typeof FormikValuesTemplate) => {
        updateProject
            .mutateAsync(
                { id: projectId, data: values },
                {
                    onError: (err) => {
                        alert(`${err.code} ${err.message}`);
                    }
                }
            )
            .then(() => {
                notification?.success({
                    message: 'Changes saved!',
                    placement: 'topRight',
                    duration: 5
                });
                navigate(`/projects/${projectId}`);
            });
    };
    useEffect(() => {
        if (project.isSuccess) {
            const data = project.data.data;
            const updateData: Omit<typeof data, 'id' | 'total_cost' | 'total_transactions'> = data;
            formikDetails.setValues({ ...updateData, org_id: data.org_id || '' });
        }
    }, [project.status]);
    const formikDetails = useFormik({
        initialValues: FormikValuesTemplate,
        onSubmit: async (values) => {
            submit(values);
        },
        validationSchema: projectSchema,
        validateOnChange: false
    });
    if (project.isError)
        return (
            <>
                <div>An error has occurred {project.error.code}</div>
                {console.error(project.error)}
            </>
        );
    if (project.isLoading)
        return (
            <Spin
                size="large"
                className="absolute top-1/2 left-1/2 -transtaction-x-1/2 -transtaction-y-1/2"
            />
        );
    if (project.isSuccess) {
        const data = project.data.data;
        return (
            <Flex gap={24} vertical>
                <HeaderContainer height={100}>
                    <Flex vertical justify="space-between">
                        <Breadcrumb
                            className="ms-1"
                            items={[
                                {
                                    title: <Link to={'/projects'}>Projects</Link>
                                },
                                {
                                    title: data.name
                                },
                                {
                                    title: 'Edit project details'
                                }
                            ]}
                        />
                        <Title level={1} className="h4 m-0">
                            Edit project details
                        </Title>
                    </Flex>
                </HeaderContainer>
                <div className="px-[24px]">
                    <ProjectDetails formik={formikDetails} />
                    <Flex
                        justify="flex-end"
                        gap={16}
                        className="px-[24px] py-[16px] mt-[12px] bg-Background/colorBgBase border border-solid border-Border/colorBorderSecondary rounded-[8px]"
                    >
                        <Button
                            className="my-auto"
                            size="large"
                            type="text"
                            onClick={() => {
                                navigate(`/projects/${projectId}`);
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
                                formikDetails.validateForm().then((errors) => {
                                    if (Object.keys(errors).length === 0) {
                                        formikDetails.submitForm();
                                    }
                                });
                            }}
                        >
                            Save
                        </Button>
                    </Flex>
                </div>
            </Flex>
        );
    }
};
export default UpdateProject;
