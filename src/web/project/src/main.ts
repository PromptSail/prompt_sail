import 'bootstrap';
import api from './api/api';

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

// document.body.appendChild(btn);
