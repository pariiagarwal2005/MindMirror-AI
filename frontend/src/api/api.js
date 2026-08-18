import axios from "axios";


const API = axios.create({

    baseURL: "http://127.0.0.1:8000",

    headers: {
        "Content-Type": "application/json"
    }

});


// =====================================================
// ADD JWT TOKEN TO EVERY REQUEST
// =====================================================

API.interceptors.request.use(

    (config) => {

        const token =
            localStorage.getItem("access_token");


        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }


        return config;

    },


    (error) => {

        return Promise.reject(error);

    }

);


// =====================================================
// HANDLE AUTHENTICATION ERRORS
// =====================================================

API.interceptors.response.use(

    (response) => {

        return response;

    },


    (error) => {

        if (error.response?.status === 401) {

            console.log(
                "MindMirror authentication failed."
            );

        }


        return Promise.reject(error);

    }

);


export default API;