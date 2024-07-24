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

export const loginSchema = yup.object().shape({
    username: yup.string().required('This field is required'),
    password: yup.string().required('This field is required')
});

export const registerSchema = yup.object().shape({
    email: yup.string().email('Enter a valid email').required('This field is required'),
    given_name: yup.string().required('This field is required'),
    family_name: yup.string().required('This field is required'),
    username: yup.string().required('This field is required'),
    password: yup
        .string()
        .min(8, 'Password must be at least 8 characters')
        .required('This field is required'),
    repeated_password: yup
        .string()
        .oneOf([yup.ref('password'), undefined], 'Passwords must match')
        .required('This field is required')
});
