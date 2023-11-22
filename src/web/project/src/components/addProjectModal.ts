import api from '../api/api';
import { addProjectRequest } from '../api/interfaces';

const settings = {
    target: '#addProjectModal',
    form: '#addProjectModal form'
};

const DOM = {
    target: document.body.querySelector(settings.target),
    form: document.body.querySelector(`${settings.target} ${settings.form}`)
};

const addProject = {
    DOM: {},
    init: () => {
        if (document.querySelectorAll(settings.target).length > 0) {
            addProject.catchDOM();
            addProject.submit();
        }
    },
    submit: () => {
        DOM.form.addEventListener('submit', (e: SubmitEvent) => {
            e.preventDefault();
            const formData = new FormData(e.target as HTMLFormElement);
            console.log(formData.get('name'));
            const formDataObject: { [key: string]: string } = {};
            formData.forEach((value, key) => {
                formDataObject[key] = value.toString();
            });
            const data: addProjectRequest = {
                name: formDataObject['name'],
                slug: formDataObject['slug'],
                description: formDataObject['description'],
                ai_providers: [
                    {
                        api_base: formDataObject['api_base'],
                        provider_name: formDataObject['provider_name'],
                        model_name: formDataObject['model_name']
                    }
                ],
                tags: formDataObject['tags'].replace(' ', '').split(','),
                org_id: formDataObject['org_id']
            };
            console.log(data);
            api.addProject(data)
                .then((e) => console.log(e))
                .catch((err) => console.error(err));
        });
    },
    catchDOM: () => {
        (DOM.target = document.body.querySelector(settings.target)),
            (DOM.form = document.body.querySelector(settings.form));
    }
};

export default addProject;
