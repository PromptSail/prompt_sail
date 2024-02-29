import { ReactNode } from 'react';

const Helper: React.FC<{ children: ReactNode }> = ({ children }) => {
    return (
        <></>
        // <OverlayTrigger placement="top" overlay={<Tooltip>{children}</Tooltip>}>
        //     <span
        //         style={{
        //             position: 'absolute',
        //             right: '-25px',
        //             top: '5%',
        //             display: 'inline-block',
        //             transform: 'scale(.7)',
        //             background: 'var(--bs-gray-500)',
        //             color: '#FFF',
        //             height: '19px',
        //             borderRadius: '50%',
        //             aspectRatio: '1/1',
        //             padding: '.5em',
        //             lineHeight: '5px',
        //             margin: 'auto',
        //             fontWeight: 'bold'
        //         }}
        //     >
        //         ?
        //     </span>
        // </OverlayTrigger>
    );
};

export default Helper;
