import { useNavigate } from "react-router-dom";


function History() {

    const navigate = useNavigate();


    return (

        <div className="
            min-h-screen
            bg-[#faf8ff]
            flex
            items-center
            justify-center
            px-6
        ">

            <div className="
                bg-white
                rounded-3xl
                border
                border-purple-100
                shadow-sm
                p-10
                max-w-lg
                text-center
            ">

                <div className="text-5xl mb-5">
                    💬
                </div>


                <h1 className="
                    text-2xl
                    font-bold
                    text-gray-800
                ">
                    Your conversations are now in Recents
                </h1>


                <p className="
                    text-gray-500
                    mt-3
                    leading-relaxed
                ">
                    You can access all your conversations from
                    the Recents section inside MindMirror.
                </p>


                <button
                    onClick={() =>
                        navigate("/journal")
                    }
                    className="
                        mt-7
                        bg-purple-600
                        text-white
                        px-6
                        py-3
                        rounded-xl
                        font-medium
                        hover:bg-purple-700
                        transition
                    "
                >
                    Open MindMirror
                </button>

            </div>

        </div>

    );

}


export default History;