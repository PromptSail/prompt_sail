import { Popover, Space, Tag } from 'antd';

export const TagsContainer: React.FC<{ tags: string[] }> = ({ tags }) => (
    <Space size={0} className="min-w-40">
        {tags
            .filter((_el, id) => id < 3)
            .map((e, id) => (
                <Tag key={id} color="magenta">
                    {e}
                </Tag>
            ))}
        {tags.length > 3 && (
            <Popover
                content={tags.map((e, id) => (
                    <Tag key={id} color="magenta">
                        {e}
                    </Tag>
                ))}
                title="Tags"
                trigger="hover"
            >
                <Tag style={{ cursor: 'pointer' }}>...</Tag>
            </Popover>
        )}
    </Space>
);
