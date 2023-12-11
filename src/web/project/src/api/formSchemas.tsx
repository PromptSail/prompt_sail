import * as yup from 'yup';
export const addProjectSchema = yup.object().shape({
    name: yup.string().required('To pole jest wymagane'),
    slug: yup.string().required('To pole jest wymagane'),
    description: yup.string().max(280, 'Za długie').required('To pole jest wymagane'),
    api_base: yup
        .string()
        .url('Proszę wpisać poprawny adres url')
        .required('To pole jest wymagane'),
    ai_model_name: yup.string().required('To pole jest wymagane'),
    tags: yup.string().required('To pole jest wymagane')
});
