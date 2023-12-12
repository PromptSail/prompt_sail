import { useState } from 'react';
import { Button, Modal } from 'react-bootstrap';
import { useDeleteProject } from '../../api/queries';

interface Props {
    name: string;
    projectId: string;
}

const DeleteProject: React.FC<Props> = ({ name, projectId }) => {
    const [isShow, setShow] = useState(false);
    const deleteProject = useDeleteProject();
    return (
        <>
            <Button variant="primary" onClick={() => setShow((e) => !e)}>
                Delete
            </Button>
            <Modal show={isShow} onHide={() => setShow((e) => !e)}>
                <Modal.Header closeButton>
                    <Modal.Title>Delete {name}</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <p>Are you sure you want to delete this project?</p>
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShow((e) => !e)}>
                        No
                    </Button>
                    <Button
                        variant="primary"
                        onClick={() => {
                            deleteProject.mutateAsync(projectId);
                        }}
                    >
                        Yes
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};
export default DeleteProject;
