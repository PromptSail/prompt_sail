import 'bootstrap';
import api from './api/api';

import addProject from './components/addProjectModal';

addProject.init();
const product = () => {
    api.getProjects()
        .then((el) => {
            console.log(el);
        })
        .catch((err) => {
            console.log(err);
        });
};
const btn = document.createElement('button');
btn.innerText = 'get_projects';
btn.addEventListener('click', () => {
    console.log(product());
});

// api.addProject(data)
//     .then((el) => console.log(el))
//     .catch((err) => console.log(err));

// document.body.appendChild(btn);
