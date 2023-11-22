import api from '../../api/api';
import { addProjectRequest } from '../../api/interfaces';

const settings = {
    target: '#addProjectModal',
    form: '#addProjectModal form'
};

const DOM = {
    target: document.body.querySelector(settings.target),
    form: document.body.querySelector(`${settings.target} ${settings.form}`)
};

const addProject = {
    DOM: {} as { [key: string]: HTMLElement },
    init: function () {
        if (document.querySelectorAll(settings.target).length > 0) {
            this.catchDOM(settings);
            this.submit();
        }
    },
    submit: function () {
        this.DOM.form.addEventListener('submit', (e: SubmitEvent) => {
            e.preventDefault();
            const formData = new FormData(e.target as HTMLFormElement);
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
                tags: formDataObject['tags'].replace(/\s/g, '').split(','),
                org_id: formDataObject['org_id']
            };
            api.addProject(data)
                .then((e) => window.location.reload())
                .catch((err) => console.error(err));
        });
    },
    catchDOM: function (sets: { [key: string]: string }) {
        this.DOM.target = document.body.querySelector(sets.target);
        this.DOM.form = document.body.querySelector(sets.form);
    }
};

export default addProject;
