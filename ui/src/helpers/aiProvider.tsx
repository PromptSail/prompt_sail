import slugify from 'slugify';

export const toSlug = (text: string) => {
    const newText = text.replace(/^\d+|[@*()+:'"~]/g, '');
    return slugify(newText, {
        replacement: '-',
        lower: true
    });
};

export const makeUrl = (slug: string, name: string) => {
    return `${window.location.host + '/api' || import.meta.env.BACKEND_URL}/${
        toSlug(slug) || '<slug>'
    }/${toSlug(name) || '<name>'}`;
};
