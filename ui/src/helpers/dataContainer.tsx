import { Popover, Space, Tag } from 'antd';
import { useEffect, useRef, useState } from 'react';

interface Props {
    tags: string[];
    classname?: string;
}

export const TagsContainer: React.FC<Props> = ({ tags, classname }) => {
    const containerRef = useRef(null);
    const gap = 8;
    const tagsJSX: JSX.Element[] = tags.map((el, id) => (
        <Tag className="m-0" key={id}>
            {el}
        </Tag>
    ));
    const [visibleTags, setVisibleTags] = useState([] as JSX.Element[]);
    const [isWidthLoading, setWidthLading] = useState(true);
    useEffect(() => {
        const handleTagsWidth = () => {
            let containerW = 0;
            const visibleChildren: JSX.Element[] = [];
            if (containerRef.current) {
                const container = containerRef.current as HTMLDivElement;
                const hiddenTags = container.querySelectorAll('.not-visible-tags')[0];
                if (hiddenTags) {
                    containerW = container.getBoundingClientRect().width;
                    hiddenTags.childNodes.forEach((el) => {
                        const width = (el as HTMLDivElement).getBoundingClientRect().width;
                        containerW -= width;
                        if (containerW - (gap * visibleChildren.length + 40) > 0)
                            visibleChildren.push(
                                <Tag className="m-0" key={visibleChildren.length}>
                                    {el.textContent}
                                </Tag>
                            );
                        else return;
                    });
                    setVisibleTags(visibleChildren);
                    setWidthLading(false);
                }
            }
        };
        handleTagsWidth();
        setWidthLading(false);
        window.addEventListener('resize', () => {
            setWidthLading(true);
            handleTagsWidth();
        });
        return () =>
            window.removeEventListener('resize', () => {
                setWidthLading(true);
                handleTagsWidth();
            });
    }, []);
    return (
        <Space ref={containerRef} size={gap} className={`min-w-40 ${classname}`}>
            {visibleTags.map((el) => el)}
            {visibleTags.length < tags.length && (
                <Popover
                    content={
                        <Space size={gap} className="flex-wrap">
                            {tagsJSX}
                        </Space>
                    }
                    title="Tags"
                    trigger="hover"
                >
                    <Tag className="cursor-pointer m-0">+{tags.length - visibleTags.length}</Tag>
                </Popover>
            )}
            {isWidthLoading && (
                <div className="not-visible-tags absolute opacity-0 -top-5">
                    {tagsJSX.map((el) => el)}
                </div>
            )}
        </Space>
    );
};
