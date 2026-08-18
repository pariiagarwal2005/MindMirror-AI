import { useEffect } from "react";
import { useNavigate } from "react-router-dom";


function Dashboard() {

    const navigate = useNavigate();


    useEffect(() => {

        navigate(
            "/journal",
            {
                replace: true
            }
        );

    }, [navigate]);


    return (

        <div className="
            min-h-screen
            bg-[#faf8ff]
            flex
            items-center
            justify-center
        ">

            <div className="
                text-center
                text-gray-500
            ">

                <div className="text-4xl mb-3">
                    💜
                </div>

                Opening MindMirror...

            </div>

        </div>

    );

}


export default Dashboard;