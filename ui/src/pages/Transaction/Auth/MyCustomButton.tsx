const MyCustomButton: React.FC<{ onClick: (arg: any) => void; children: string }> = ({
    onClick,
    children
}) => {
    return (
        <button
            style={{
                backgroundColor: 'blue',
                color: 'white',
                borderRadius: '5px',
                padding: '10px 20px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '16px'
            }}
            onClick={onClick}
        >
            {children}
        </button>
    );
};

export default MyCustomButton;
