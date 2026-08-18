import { useState } from "react";
import API from "../api/api";


function Register(){

    const [username,setUsername] = useState("");
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");



    const registerUser = async()=>{


        try{


            const response = await API.post(
                "/register",
                null,
                {
                    params:{
                        username,
                        email,
                        password
                    }
                }
            );


            alert("Account created successfully");


            console.log(response.data);


        }
        catch(error){

            console.log(error.response.data);


            alert(
                error.response.data.detail ||
                "Registration failed"
            );

        }

    }



    return(

        <div className="min-h-screen flex items-center justify-center">


            <div className="bg-white shadow-lg p-10 rounded-xl">


                <h1 className="text-3xl font-bold mb-6">
                    Create Account
                </h1>



                <input

                className="border p-3 block mb-4 w-80"

                placeholder="Username"

                onChange={(e)=>
                    setUsername(e.target.value)
                }

                />



                <input

                className="border p-3 block mb-4 w-80"

                placeholder="Email"

                onChange={(e)=>
                    setEmail(e.target.value)
                }

                />



                <input

                className="border p-3 block mb-4 w-80"

                placeholder="Password"

                type="password"

                onChange={(e)=>
                    setPassword(e.target.value)
                }

                />



                <button

                onClick={registerUser}

                className="bg-purple-600 text-white px-6 py-3 rounded-lg"

                >

                    Register

                </button>



            </div>


        </div>

    )

}


export default Register;