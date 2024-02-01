import * as yup from 'yup';
export const projectSchema = yup.object().shape({
    name: yup.string().min(3, 'Too short').max(50, 'Too long').required('This field is required'),
    slug: yup.string().min(3, 'Too short').max(50, 'Too long').required('This field is required'),
    description: yup.string().max(280, 'Too long').required('This field is required'),
    tags: yup.string().required('This field is required'),
    ai_providers: yup.array().min(1, 'You need to add at least one AI Provider')
});

export const providerSchema = yup.object().shape({
    api_base: yup.string().url('Enter a valid url').required('This field is required'),
    provider_name: yup.string().required('This field is required'),
    deployment_name: yup
        .string()
        .min(3, 'Too short')
        .max(50, 'Too long')
        .required('This field is required'),
    description: yup.string()
});
