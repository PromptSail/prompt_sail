import axios from 'axios';

const client = axios.create({
    // baseURL: 'http://promptsail.local', // blocked by CORS
    headers: {
        'Content-Type': 'application/json'
    }
});

export default client;
