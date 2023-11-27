import axios from 'axios';

const client = axios.create({
    // baseURL: 'http://promptsail.local', // blocked by CORS
    baseURL: 'api',
    headers: {
        // Accept: 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
    }
});

export default client;
