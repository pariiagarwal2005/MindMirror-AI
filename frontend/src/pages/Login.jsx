import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/api";

function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    const handleLogin = async (event) => {

        event.preventDefault();

        setError("");
        setLoading(true);


        try {

            const formData = new URLSearchParams();

            formData.append(
                "username",
                email
            );

            formData.append(
                "password",
                password
            );


            const response = await API.post(
                "/login",
                formData,
                {
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    }
                }
            );


            console.log(
                "LOGIN RESPONSE:",
                response.data
            );


            const token =
                response.data.access_token;


            if (!token) {

                throw new Error(
                    "Login succeeded but no access token was returned."
                );
            }


            // =================================================
            // SAVE TOKEN
            // =================================================

            localStorage.setItem(
                "access_token",
                token
            );


            console.log(
                "ACCESS TOKEN SAVED:",
                localStorage.getItem("access_token")
            );


            // =================================================
            // GO TO DASHBOARD
            // =================================================

            navigate("/dashboard");

        }

        catch (error) {

            console.log(
                "LOGIN ERROR:",
                error
            );


            if (error.response?.data?.detail) {

                setError(
                    error.response.data.detail
                );

            }

            else {

                setError(
                    "Unable to login. Please try again."
                );
            }
        }

        finally {

            setLoading(false);
        }
    };


    return (

        <div className="min-h-screen bg-purple-50 flex items-center justify-center px-4">

            <div className="bg-white w-full max-w-md rounded-2xl shadow-sm p-8">

                <div className="text-center mb-8">

                    <div className="text-5xl mb-4">
                        💜
                    </div>

                    <h1 className="text-3xl font-bold text-purple-700">
                        Welcome Back
                    </h1>

                    <p className="text-gray-500 mt-2">
                        Sign in to continue your MindMirror journey.
                    </p>

                </div>


                <form
                    onSubmit={handleLogin}
                    className="space-y-5"
                >

                    <div>

                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(event) =>
                                setEmail(event.target.value)
                            }
                            placeholder="Enter your email"
                            required
                            className="w-full border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-400"
                        />

                    </div>


                    <div>

                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(event) =>
                                setPassword(event.target.value)
                            }
                            placeholder="Enter your password"
                            required
                            className="w-full border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-400"
                        />

                    </div>


                    {error && (

                        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm">
                            {error}
                        </div>

                    )}


                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-purple-600 text-white py-3 rounded-xl hover:bg-purple-700 disabled:opacity-50"
                    >

                        {loading
                            ? "Logging in..."
                            : "Login"
                        }

                    </button>

                </form>


                <p className="text-center text-sm text-gray-500 mt-6">

                    Don't have an account?

                    <button
                        onClick={() =>
                            navigate("/register")
                        }
                        className="text-purple-600 font-medium ml-1"
                    >
                        Register
                    </button>

                </p>

            </div>

        </div>
    );
}

export default Login;