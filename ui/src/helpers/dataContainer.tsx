import { Popover, Space, Tag } from 'antd';

interface Props {
    tags: string[];
    classname?: string;
}

export const TagsContainer: React.FC<Props> = ({ tags, classname }) => (
    <Space size={0} className={`min-w-40 ${classname}`}>
        {tags
            .filter((_el, id) => id < 3)
            .map((e, id) => (
                <Tag key={id}>{e}</Tag>
            ))}
        {tags.length > 3 && (
            <Popover
                content={tags.map((e, id) => (
                    <Tag key={id}>{e}</Tag>
                ))}
                title="Tags"
                trigger="hover"
            >
                <Tag style={{ cursor: 'pointer' }}>...</Tag>
            </Popover>
        )}
    </Space>
);
