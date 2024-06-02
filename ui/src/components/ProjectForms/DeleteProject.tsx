import { useDeleteProject } from '../../api/queries';
import { Button, Typography } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import { Context } from '../../context/Context';
import { useContext } from 'react';

const { Paragraph } = Typography;

interface Props {
    name: string;
    projectId: string;
}

const DeleteProject: React.FC<Props> = ({ name, projectId }) => {
    const { notification, modal } = useContext(Context);
    const deleteProject = useDeleteProject();
    return (
        <Button
            className="my-auto z-10"
            icon={<DeleteOutlined />}
            onClick={() => {
                if (modal)
                    modal.confirm({
                        title: 'Delete project',
                        icon: <></>,
                        content: (
                            <>
                                <Paragraph className="!m-0">
                                    Are you sure you want to delete "{name}" project?
                                </Paragraph>
                                <Paragraph className="!m-0">You will looseall your data.</Paragraph>
                            </>
                        ),
                        onOk() {
                            deleteProject.mutateAsync(projectId).then(() => {
                                if (notification)
                                    notification.success({
                                        message: 'Project deleted!',
                                        placement: 'topRight',
                                        duration: 5
                                    });
                            });
                        },
                        okButtonProps: {
                            danger: true,
                            icon: <DeleteOutlined />
                        },
                        okText: 'Delete',
                        closable: true
                    });
            }}
        >
            Delete
        </Button>
    );
};
export default DeleteProject;
