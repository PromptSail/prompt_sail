import { useDeleteProject } from '../../api/queries';
import { Button, Modal } from 'antd';
import { ExclamationCircleFilled } from '@ant-design/icons';
const { confirm } = Modal;

interface Props {
    name: string;
    projectId: string;
}

const DeleteProject: React.FC<Props> = ({ name, projectId }) => {
    const deleteProject = useDeleteProject();
    return (
        <>
            <Button
                danger
                onClick={() =>
                    confirm({
                        title: name,
                        icon: <ExclamationCircleFilled />,
                        content: 'Are you sure you want to delete this project?',
                        onOk() {
                            deleteProject.mutateAsync(projectId);
                        }
                    })
                }
            >
                Delete
            </Button>
        </>
    );
};
export default DeleteProject;
