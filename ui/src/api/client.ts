import axios from 'axios';

const client = axios.create({
    baseURL: `http://localhost/api`,
    headers: {
        // Accept: 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
    }
});

// client.interceptors.request.use(
//     function (config) {
//         // Modyfikacje przed wysłaniem zapytania
//         return config;
//     },
//     function (error) {
//         // Obsługa błędów związanych z zapytaniem
//         return Promise.reject(error);
//     }
// );

// client.interceptors.response.use(
//     function (response) {
//         // Modyfikacje przed obsługą odpowiedzi
//         return response;
//     },
//     function (error) {
//         // Obsługa błędów związanych z odpowiedzią
//         return Promise.reject(error);
//     }
// );

export default client;
