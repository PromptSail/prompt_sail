import axios from 'axios';

const client = axios.create({
    baseURL: 'http://localhost:8000', // blocked by CORS
    headers: {
        'Content-Type': 'application/json'
    }
});

export default client;
