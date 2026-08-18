import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";


function Home() {

    const navigate = useNavigate();


    return (

        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">

            <Navbar />


            <section className="flex flex-col items-center justify-center text-center mt-32">


                <h1 className="text-6xl font-bold text-gray-800">

                    Understand Yourself
                    <br />

                    With AI

                </h1>


                <p className="mt-6 text-xl text-gray-600 max-w-xl">

                    MindMirror AI helps you reflect on your emotions,
                    understand your mood patterns and build better
                    self-awareness.

                </p>


                <button
                    onClick={() => navigate("/journal")}
                    className="mt-10 bg-purple-600 text-white px-8 py-3 rounded-xl text-lg hover:bg-purple-700 transition"
                >

                    Start Your Reflection 💜

                </button>


            </section>


        </div>

    );

}


export default Home;