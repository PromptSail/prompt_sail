import { useEffect, useState } from 'react';

const isBase64 = (str: string) => {
    const base64Regex = /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/;
    return base64Regex.test(str);
};
const isLink = (str: string) => {
    try {
        new URL(str);
        return true;
    } catch (error) {
        return false;
    }
};

export const useHandleTransactionImage = (src: string) => {
    const [imageError, setImageError] = useState(false);
    useEffect(() => {
        if (!isBase64(src) && !isLink(src)) {
            setImageError(true);
        }
    }, [isBase64(src), isLink(src)]);
    return imageError ? (
        src
    ) : (
        <img
            src={isBase64(src) ? `data:image/png;base64,${src}` : src}
            alt="image"
            onError={() => {
                setImageError(true);
            }}
        />
    );
};
