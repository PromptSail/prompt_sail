import api from '../../api/api';
import { updateProjectRequest, getProjectResponse } from '../../api/interfaces';

const settings = {
    target: '#updateProjectModal',
    form: '#updateProjectModal form',

    id: 'data-projectId',
    name: '[name="name"]',
    slug: '[name="slug"]',
    description: '[name="description"]',
    api_base: '[name="api_base"]',
    provider_name: '[name="provider_name"]',
    model_name: '[name="model_name"]',
    tags: '[name="tags"]',
    org_id: '[name="org_id"]'
};

const updateProject = {
    DOM: {} as { [key: string]: HTMLElement },
    init: function () {
        if (document.querySelectorAll(settings.target).length > 0) {
            updateProject.catchDOM(settings);
            updateProject.load();
            updateProject.submit();
        }
    },
    load: function () {
        this.id = this.DOM.target.getAttribute(settings.id);
        api.getProject(this.id)
            .then((response) => {
                const data = response.data as getProjectResponse;
                this.DOM.name.value = data.name;
                this.DOM.slug.value = data.slug;
                this.DOM.description.value = data.description;
                this.DOM.api_base.value = data.ai_providers[0].api_base;
                this.DOM.provider_name.value = data.ai_providers[0].provider_name;
                this.DOM.model_name.value = data.ai_providers[0].model_name;
                this.DOM.tags.value = data.tags;
                this.DOM.org_id.value = data.org_id;
            })
            .catch((err) => console.error(err));
    },
    submit: function () {
        this.DOM.form.addEventListener('submit', (e: SubmitEvent) => {
            e.preventDefault();
            const formData = new FormData(e.target as HTMLFormElement);
            console.log(formData.get('name'));
            const formDataObject: { [key: string]: string } = {};
            formData.forEach((value, key) => {
                formDataObject[key] = value.toString();
            });
            const data: updateProjectRequest = {
                id: this.id,
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
            api.updateProject(this.id, data)
                .then((e) => window.location.reload())
                .catch((err) => console.error(err));
        });
    },
    catchDOM: function (sets: { [key: string]: string }) {
        this.DOM.target = document.body.querySelector(sets.target);
        this.DOM.form = document.body.querySelector(sets.form);
        this.DOM.name = document.body.querySelector(`${sets.form} ${sets.name}`);
        this.DOM.slug = document.body.querySelector(`${sets.form} ${sets.slug}`);
        this.DOM.description = document.body.querySelector(`${sets.form} ${sets.description}`);
        this.DOM.api_base = document.body.querySelector(`${sets.form} ${sets.api_base}`);
        this.DOM.provider_name = document.body.querySelector(`${sets.form} ${sets.provider_name}`);
        this.DOM.model_name = document.body.querySelector(`${sets.form} ${sets.model_name}`);
        this.DOM.tags = document.body.querySelector(`${sets.form} ${sets.tags}`);
        this.DOM.org_id = document.body.querySelector(`${sets.form} ${sets.org_id}`);
    }
};

export default updateProject;
