import * as yup from 'yup';
export const projectSchema = yup.object().shape({
    name: yup
        .string()
        .min(3, 'Length must be between 3 and 50 characters')
        .max(50, 'Length must be between 3 and 50 characters')
        .required('This field is required'),
    slug: yup
        .string()
        .min(3, 'Length must be between 3 and 50 characters')
        .max(50, 'Length must be between 3 and 50 characters')
        .required('This field is required'),
    description: yup.string().max(280, 'Maximum length is 280 characters'),
    tags: yup.array().of(yup.string()),
    owner: yup.string().required('This field is required')
});

export const providerSchema = yup.object().shape({
    api_base: yup.string().url('Enter a valid url').required('This field is required'),
    provider_name: yup.string().required('This field is required'),
    deployment_name: yup
        .string()
        .min(3, 'Length must be between 3 and 50 characters')
        .max(50, 'Length must be between 3 and 50 characters')
        .required('This field is required'),
    description: yup.string()
});
