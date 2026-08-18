import axios from "axios";


const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000";


const API = axios.create({

    baseURL:
        API_URL,

    headers: {

        "Content-Type":
            "application/json"

    }

});


// =====================================================
// ADD JWT TOKEN
// =====================================================

API.interceptors.request.use(

    (config) => {

        const token =
            localStorage.getItem(
                "access_token"
            );


        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }


        return config;

    },


    (error) => {

        return Promise.reject(
            error
        );

    }

);


// =====================================================
// RESPONSE HANDLING
// =====================================================

API.interceptors.response.use(

    (response) => {

        return response;

    },


    (error) => {

        if (
            error.response?.status ===
            401
        ) {

            console.log(
                "MindMirror authentication failed."
            );

        }


        return Promise.reject(
            error
        );

    }

);


export default API;