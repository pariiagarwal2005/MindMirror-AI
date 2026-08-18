import React, {
    useEffect,
    useRef,
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import API from "../api/api";


// =====================================================
// JOURNAL PAGE
// =====================================================

function Journal() {

    const navigate = useNavigate();

    const messagesEndRef =
        useRef(null);

    const messageInputRef =
        useRef(null);


    // =====================================================
    // STATE
    // =====================================================

    const [conversations, setConversations] =
        useState([]);

    const [activeConversation, setActiveConversation] =
        useState(null);

    const [messages, setMessages] =
        useState([]);

    const [message, setMessage] =
        useState("");

    const [loading, setLoading] =
        useState(true);

    const [sending, setSending] =
        useState(false);

    const [error, setError] =
        useState("");

    const [sidebarOpen, setSidebarOpen] =
        useState(true);


    // =====================================================
    // LOAD CONVERSATIONS WHEN PAGE OPENS
    // =====================================================

    useEffect(() => {

        loadConversations();

    }, []);


    // =====================================================
    // AUTO SCROLL
    // =====================================================

    useEffect(() => {

        if (messagesEndRef.current) {

            messagesEndRef.current.scrollIntoView({
                behavior: "smooth"
            });

        }

    }, [messages, sending]);


    // =====================================================
    // LOAD ALL CONVERSATIONS
    // =====================================================

    const loadConversations = async () => {

        try {

            setLoading(true);
            setError("");

            const response =
                await API.get(
                    "/chat/conversations"
                );


            const backendConversations =
                response.data.conversations || [];


            const formattedConversations =
                backendConversations
                    .filter(
                        (conversation) =>
                            conversation.conversation_id
                    )
                    .map(
                        (conversation) => ({

                            id:
                                conversation.conversation_id,

                            conversation_id:
                                conversation.conversation_id,

                            title:
                                conversation.title ||
                                "New conversation",

                            created_at:
                                conversation.created_at,

                            updated_at:
                                conversation.updated_at ||
                                conversation.created_at,

                            message_count:
                                conversation.message_count || 0

                        })
                    );


            setConversations(
                formattedConversations
            );


        }

        catch (error) {

            console.log(
                "LOAD CONVERSATIONS ERROR:",
                error
            );


            if (
                error.response?.status === 401
            ) {

                localStorage.removeItem(
                    "access_token"
                );

                navigate("/login");

                return;

            }


            setError(
                error.response?.data?.detail ||
                "Unable to load your conversations."
            );

        }

        finally {

            setLoading(false);

        }

    };


    // =====================================================
    // CREATE NEW CHAT
    // =====================================================

    const createNewChat = () => {

        setActiveConversation(null);

        setMessages([]);

        setMessage("");

        setError("");


        // Reset textarea height

        if (messageInputRef.current) {

            messageInputRef.current.style.height =
                "auto";

        }


        if (
            window.innerWidth < 768
        ) {

            setSidebarOpen(false);

        }

    };


    // =====================================================
    // LOAD ONE CONVERSATION
    // =====================================================

    const loadConversation = async (
        conversationId
    ) => {

        if (
            !conversationId ||
            conversationId === "undefined" ||
            conversationId === "null"
        ) {

            console.log(
                "INVALID CONVERSATION ID:",
                conversationId
            );

            return;

        }


        try {

            setError("");

            const response =
                await API.get(
                    `/chat/conversations/${encodeURIComponent(
                        conversationId
                    )}`
                );


            const data =
                response.data;


            const formattedMessages =
                (data.messages || []).map(
                    (item) => ({

                        id:
                            item.id,

                        role:
                            item.role,

                        content:
                            item.content,

                        created_at:
                            item.created_at

                    })
                );


            setActiveConversation({

                id:
                    data.conversation_id,

                conversation_id:
                    data.conversation_id,

                title:
                    data.title ||
                    "New conversation"

            });


            setMessages(
                formattedMessages
            );


            if (
                window.innerWidth < 768
            ) {

                setSidebarOpen(false);

            }

        }

        catch (error) {

            console.log(
                "LOAD CONVERSATION ERROR:",
                error
            );


            if (
                error.response?.status === 401
            ) {

                localStorage.removeItem(
                    "access_token"
                );

                navigate("/login");

                return;

            }


            setError(
                error.response?.data?.detail ||
                "Unable to open this conversation."
            );

        }

    };


    // =====================================================
    // SEND MESSAGE
    // =====================================================

    const sendMessage = async (
        event
    ) => {

        if (event) {

            event.preventDefault();

        }


        const trimmedMessage =
            message.trim();


        if (
            !trimmedMessage ||
            sending
        ) {

            return;

        }


        setError("");

        setSending(true);


        const temporaryMessage = {

            id:
                `user-${Date.now()}`,

            role:
                "user",

            content:
                trimmedMessage,

            created_at:
                new Date().toISOString()

        };


        setMessages(
            (previous) => [
                ...previous,
                temporaryMessage
            ]
        );


        setMessage("");


        // Reset textarea height after sending

        if (messageInputRef.current) {

            messageInputRef.current.style.height =
                "auto";

        }


        try {

            let requestUrl =
                `/chat?message=${encodeURIComponent(
                    trimmedMessage
                )}`;


            if (
                activeConversation?.id
            ) {

                requestUrl +=
                    `&conversation_id=${encodeURIComponent(
                        activeConversation.id
                    )}`;

            }


            const response =
                await API.post(
                    requestUrl
                );


            const conversationId =
                response.data.conversation_id;


            const assistantMessage = {

                id:
                    response.data.message_id ||
                    `assistant-${Date.now()}`,

                role:
                    "assistant",

                content:
                    response.data.reply,

                created_at:
                    new Date().toISOString()

            };


            setMessages(
                (previous) => [
                    ...previous,
                    assistantMessage
                ]
            );


            if (
                conversationId
            ) {

                const newTitle =
                    response.data.title ||
                    (
                        trimmedMessage.length > 45
                            ? `${trimmedMessage.substring(
                                0,
                                45
                            )}...`
                            : trimmedMessage
                    );


                setActiveConversation(
                    (previous) => ({

                        id:
                            conversationId,

                        conversation_id:
                            conversationId,

                        title:
                            previous?.title ||
                            newTitle

                    })
                );


                setConversations(
                    (previous) => {

                        const existing =
                            previous.find(
                                (conversation) =>
                                    conversation.id ===
                                    conversationId
                            );


                        if (existing) {

                            return previous
                                .map(
                                    (conversation) => {

                                        if (
                                            conversation.id ===
                                            conversationId
                                        ) {

                                            return {

                                                ...conversation,

                                                title:
                                                    conversation.title ||
                                                    newTitle,

                                                updated_at:
                                                    new Date().toISOString(),

                                                message_count:
                                                    (
                                                        conversation.message_count ||
                                                        0
                                                    ) + 2

                                            };

                                        }

                                        return conversation;

                                    }
                                )
                                .sort(
                                    (a, b) =>
                                        new Date(
                                            b.updated_at
                                        ) -
                                        new Date(
                                            a.updated_at
                                        )
                                );

                        }


                        return [

                            {

                                id:
                                    conversationId,

                                conversation_id:
                                    conversationId,

                                title:
                                    newTitle,

                                created_at:
                                    new Date().toISOString(),

                                updated_at:
                                    new Date().toISOString(),

                                message_count:
                                    2

                            },

                            ...previous

                        ];

                    }
                );

            }

        }

        catch (error) {

            console.log(
                "CHAT ERROR:",
                error
            );


            setMessages(
                (previous) =>
                    previous.filter(
                        (item) =>
                            item.id !==
                            temporaryMessage.id
                    )
            );


            if (
                error.response?.status === 401
            ) {

                localStorage.removeItem(
                    "access_token"
                );

                navigate("/login");

                return;

            }


            setError(
                error.response?.data?.detail ||
                "Something went wrong while sending your message."
            );

        }

        finally {

            setSending(false);

        }

    };


    // =====================================================
    // DELETE CONVERSATION
    // =====================================================

    const deleteConversation = async (
        conversationId,
        event
    ) => {

        if (event) {

            event.stopPropagation();

        }


        if (
            !conversationId
        ) {

            return;

        }


        try {

            await API.delete(
                `/chat/conversations/${encodeURIComponent(
                    conversationId
                )}`
            );


            setConversations(
                (previous) =>
                    previous.filter(
                        (conversation) =>
                            conversation.id !==
                            conversationId
                    )
            );


            if (
                activeConversation?.id ===
                conversationId
            ) {

                setActiveConversation(
                    null
                );

                setMessages([]);

            }

        }

        catch (error) {

            console.log(
                "DELETE CONVERSATION ERROR:",
                error
            );


            if (
                error.response?.status === 401
            ) {

                localStorage.removeItem(
                    "access_token"
                );

                navigate("/login");

                return;

            }


            setError(
                error.response?.data?.detail ||
                "Unable to delete this conversation."
            );

        }

    };


    // =====================================================
    // LOGOUT
    // =====================================================

    const logout = () => {

        localStorage.removeItem(
            "access_token"
        );

        navigate("/login");

    };


    // =====================================================
    // FORMAT DATE
    // =====================================================

    const formatDate = (
        date
    ) => {

        if (!date) {

            return "";

        }


        const current =
            new Date();

        const target =
            new Date(date);


        const sameDay =
            current.toDateString() ===
            target.toDateString();


        if (sameDay) {

            return target.toLocaleTimeString(
                [],
                {
                    hour: "2-digit",
                    minute: "2-digit"
                }
            );

        }


        return target.toLocaleDateString(
            [],
            {
                month: "short",
                day: "numeric"
            }
        );

    };


    // =====================================================
    // LOADING SCREEN
    // =====================================================

    if (loading) {

        return (

            <div className="
                h-screen
                bg-[#faf8ff]
                flex
                items-center
                justify-center
            ">

                <div className="text-center">

                    <div className="
                        text-4xl
                        mb-4
                    ">
                        💜
                    </div>

                    <p className="
                        text-gray-500
                    ">
                        Opening MindMirror...
                    </p>

                </div>

            </div>

        );

    }


    // =====================================================
    // MAIN UI
    // =====================================================

    return (

        <div className="
            h-screen
            w-full
            bg-[#faf8ff]
            flex
            overflow-hidden
        ">


            {/* =================================================
                MOBILE OVERLAY
            ================================================= */}

            {sidebarOpen && (

                <div
                    className="
                        fixed
                        inset-0
                        bg-black/20
                        z-20
                        md:hidden
                    "
                    onClick={() =>
                        setSidebarOpen(false)
                    }
                />

            )}


            {/* =================================================
                SIDEBAR
            ================================================= */}

            <aside
                className={`
                    fixed
                    md:relative
                    z-30
                    h-full
                    bg-white
                    border-r
                    border-purple-100
                    flex
                    flex-col
                    transition-all
                    duration-300
                    ${
                        sidebarOpen
                            ? "w-72"
                            : "w-0 md:w-0"
                    }
                    overflow-hidden
                `}
            >


                {/* =================================================
                    BRAND
                ================================================= */}

                <div className="
                    px-5
                    py-5
                    border-b
                    border-purple-100
                ">

                    <div className="
                        flex
                        items-center
                        justify-between
                    ">

                        <div>

                            <h1 className="
                                text-xl
                                font-bold
                                text-purple-700
                            ">
                                MindMirror 💜
                            </h1>

                            <p className="
                                text-xs
                                text-gray-400
                                mt-1
                            ">
                                Your space to reflect
                            </p>

                        </div>

                    </div>

                </div>


                {/* =================================================
                    NEW CHAT
                ================================================= */}

                <div className="p-4">

                    <button
                        onClick={
                            createNewChat
                        }
                        className="
                            w-full
                            flex
                            items-center
                            gap-3
                            px-4
                            py-3
                            rounded-xl
                            bg-purple-600
                            text-white
                            font-medium
                            hover:bg-purple-700
                            transition
                            shadow-sm
                        "
                    >

                        <span className="
                            text-xl
                        ">
                            +
                        </span>

                        <span>
                            New Chat
                        </span>

                    </button>

                </div>


                {/* =================================================
                    RECENTS
                ================================================= */}

                <div className="
                    flex-1
                    overflow-y-auto
                    px-3
                ">

                    <div className="
                        px-3
                        py-2
                    ">

                        <p className="
                            text-xs
                            font-semibold
                            text-gray-400
                            uppercase
                            tracking-wider
                        ">
                            Recents
                        </p>

                    </div>


                    {conversations.length === 0 && (

                        <div className="
                            px-3
                            py-6
                            text-sm
                            text-gray-400
                            text-center
                        ">
                            No conversations yet.
                        </div>

                    )}


                    <div className="
                        space-y-1
                    ">

                        {conversations.map(
                            (conversation) => (

                                <div
                                    key={
                                        conversation.id
                                    }
                                    className={`
                                        w-full
                                        rounded-xl
                                        transition
                                        group
                                        ${
                                            activeConversation?.id ===
                                            conversation.id
                                                ? "bg-purple-100"
                                                : "hover:bg-purple-50"
                                        }
                                    `}
                                >

                                    <div className="
                                        flex
                                        items-center
                                    ">


                                        {/* CHAT BUTTON */}

                                        <button
                                            onClick={() =>
                                                loadConversation(
                                                    conversation.id
                                                )
                                            }
                                            className={`
                                                flex-1
                                                text-left
                                                px-3
                                                py-3
                                                rounded-xl
                                                transition
                                                ${
                                                    activeConversation?.id ===
                                                    conversation.id
                                                        ? "text-purple-800"
                                                        : "text-gray-600"
                                                }
                                            `}
                                        >

                                            <div className="
                                                flex
                                                items-start
                                                gap-3
                                            ">

                                                <span className="
                                                    text-sm
                                                    mt-0.5
                                                ">
                                                    💬
                                                </span>


                                                <div className="
                                                    min-w-0
                                                    flex-1
                                                ">

                                                    <p className="
                                                        text-sm
                                                        font-medium
                                                        truncate
                                                    ">
                                                        {
                                                            conversation.title
                                                        }
                                                    </p>


                                                    <p className="
                                                        text-xs
                                                        text-gray-400
                                                        mt-1
                                                    ">
                                                        {
                                                            formatDate(
                                                                conversation.updated_at ||
                                                                conversation.created_at
                                                            )
                                                        }
                                                    </p>

                                                </div>

                                            </div>

                                        </button>


                                        {/* DELETE BUTTON */}

                                        <button
                                            onClick={(event) =>
                                                deleteConversation(
                                                    conversation.id,
                                                    event
                                                )
                                            }
                                            className="
                                                opacity-0
                                                group-hover:opacity-100
                                                mr-2
                                                w-8
                                                h-8
                                                rounded-lg
                                                flex
                                                items-center
                                                justify-center
                                                text-gray-400
                                                hover:bg-red-50
                                                hover:text-red-500
                                                transition
                                            "
                                            title="Delete conversation"
                                        >
                                            ×
                                        </button>

                                    </div>

                                </div>

                            )
                        )}

                    </div>

                </div>


                {/* =================================================
                    SIDEBAR BOTTOM
                ================================================= */}

                <div className="
                    p-3
                    border-t
                    border-purple-100
                ">

                    <button
                        onClick={logout}
                        className="
                            w-full
                            flex
                            items-center
                            gap-3
                            px-3
                            py-3
                            rounded-xl
                            text-gray-500
                            hover:bg-red-50
                            hover:text-red-600
                            transition
                        "
                    >

                        <span>
                            ↪
                        </span>

                        <span className="
                            text-sm
                            font-medium
                        ">
                            Logout
                        </span>

                    </button>

                </div>

            </aside>


            {/* =================================================
                MAIN AREA
            ================================================= */}

            <main className="
                flex-1
                min-w-0
                h-full
                flex
                flex-col
            ">


                {/* =================================================
                    HEADER
                ================================================= */}

                <header className="
                    h-16
                    flex-shrink-0
                    bg-white
                    border-b
                    border-purple-100
                    flex
                    items-center
                    px-4
                    md:px-6
                    gap-4
                ">

                    <button
                        onClick={() =>
                            setSidebarOpen(
                                !sidebarOpen
                            )
                        }
                        className="
                            w-10
                            h-10
                            rounded-xl
                            flex
                            items-center
                            justify-center
                            text-gray-600
                            hover:bg-purple-50
                            transition
                        "
                    >
                        ☰
                    </button>


                    <div className="
                        min-w-0
                    ">

                        <h2 className="
                            font-semibold
                            text-gray-800
                            truncate
                        ">

                            {
                                activeConversation?.title ||
                                "New conversation"
                            }

                        </h2>


                        <p className="
                            text-xs
                            text-gray-400
                        ">
                            Private conversation
                        </p>

                    </div>

                </header>


                {/* =================================================
                    CHAT MESSAGES
                ================================================= */}

                <section className="
                    flex-1
                    min-h-0
                    overflow-y-auto
                    px-4
                    md:px-8
                    py-6
                ">

                    <div className="
                        max-w-3xl
                        mx-auto
                        space-y-6
                    ">


                        {/* =================================================
                            EMPTY STATE
                        ================================================= */}

                        {messages.length === 0 && (

                            <div className="
                                min-h-full
                                flex
                                items-center
                                justify-center
                            ">

                                <div className="
                                    text-center
                                    max-w-md
                                    px-6
                                ">

                                    <div className="
                                        w-20
                                        h-20
                                        rounded-3xl
                                        bg-purple-100
                                        flex
                                        items-center
                                        justify-center
                                        text-4xl
                                        mx-auto
                                        mb-6
                                    ">
                                        💜
                                    </div>


                                    <h2 className="
                                        text-2xl
                                        font-bold
                                        text-gray-800
                                    ">
                                        How are you feeling today?
                                    </h2>


                                    <p className="
                                        text-gray-500
                                        mt-3
                                        leading-relaxed
                                    ">
                                        Talk to MindMirror about
                                        your day, your thoughts,
                                        your worries, or absolutely
                                        anything else.
                                    </p>

                                </div>

                            </div>

                        )}


                        {/* =================================================
                            MESSAGES
                        ================================================= */}

                        {messages.map(
                            (item) => (

                                <div
                                    key={
                                        item.id
                                    }
                                    className={`
                                        flex
                                        ${
                                            item.role === "user"
                                                ? "justify-end"
                                                : "justify-start"
                                        }
                                    `}
                                >


                                    {item.role === "assistant" && (

                                        <div className="
                                            w-9
                                            h-9
                                            rounded-xl
                                            bg-purple-100
                                            flex
                                            items-center
                                            justify-center
                                            mr-3
                                            mt-1
                                            flex-shrink-0
                                        ">
                                            💜
                                        </div>

                                    )}


                                    <div className="
                                        max-w-[80%]
                                    ">

                                        <div
                                            className={`
                                                px-4
                                                py-3
                                                rounded-2xl
                                                whitespace-pre-wrap
                                                leading-relaxed
                                                text-sm
                                                md:text-base
                                                ${
                                                    item.role === "user"
                                                        ? "bg-purple-600 text-white rounded-br-md"
                                                        : "bg-white text-gray-700 border border-purple-100 shadow-sm rounded-bl-md"
                                                }
                                            `}
                                        >

                                            {
                                                item.content
                                            }

                                        </div>


                                        {item.created_at && (

                                            <p
                                                className={`
                                                    text-[10px]
                                                    text-gray-400
                                                    mt-1
                                                    ${
                                                        item.role === "user"
                                                            ? "text-right"
                                                            : "text-left"
                                                    }
                                                `}
                                            >

                                                {
                                                    formatDate(
                                                        item.created_at
                                                    )
                                                }

                                            </p>

                                        )}

                                    </div>

                                </div>

                            )
                        )}


                        {/* =================================================
                            TYPING INDICATOR
                        ================================================= */}

                        {sending && (

                            <div className="
                                flex
                                justify-start
                            ">

                                <div className="
                                    w-9
                                    h-9
                                    rounded-xl
                                    bg-purple-100
                                    flex
                                    items-center
                                    justify-center
                                    mr-3
                                ">
                                    💜
                                </div>

                                <div className="
                                    bg-white
                                    border
                                    border-purple-100
                                    shadow-sm
                                    px-5
                                    py-4
                                    rounded-2xl
                                    rounded-bl-md
                                ">

                                    <div className="
                                        flex
                                        gap-1
                                    ">

                                        <span className="
                                            w-2
                                            h-2
                                            bg-purple-300
                                            rounded-full
                                            animate-bounce
                                        " />

                                        <span
                                            className="
                                                w-2
                                                h-2
                                                bg-purple-300
                                                rounded-full
                                                animate-bounce
                                            "
                                            style={{
                                                animationDelay:
                                                    "150ms"
                                            }}
                                        />

                                        <span
                                            className="
                                                w-2
                                                h-2
                                                bg-purple-300
                                                rounded-full
                                                animate-bounce
                                            "
                                            style={{
                                                animationDelay:
                                                    "300ms"
                                            }}
                                        />

                                    </div>

                                </div>

                            </div>

                        )}


                        <div
                            ref={
                                messagesEndRef
                            }
                        />

                    </div>

                </section>


                {/* =================================================
                    ERROR
                ================================================= */}

                {error && (

                    <div className="
                        flex-shrink-0
                        px-4
                        md:px-8
                    ">

                        <div className="
                            max-w-3xl
                            mx-auto
                            bg-red-50
                            border
                            border-red-100
                            text-red-600
                            px-4
                            py-3
                            rounded-xl
                            text-sm
                        ">

                            {error}

                        </div>

                    </div>

                )}


                {/* =================================================
                    INPUT
                ================================================= */}

                <div className="
                    flex-shrink-0
                    bg-white
                    border-t
                    border-purple-100
                    px-4
                    md:px-8
                    py-4
                ">

                    <form
                        onSubmit={
                            sendMessage
                        }
                        className="
                            max-w-3xl
                            mx-auto
                        "
                    >

                        <div className="
                            flex
                            items-end
                            gap-3
                            bg-[#faf8ff]
                            border
                            border-purple-100
                            rounded-2xl
                            p-2
                            shadow-sm
                            focus-within:ring-2
                            focus-within:ring-purple-200
                        ">

                            {/* =================================================
                                AUTO-GROWING TEXTAREA
                            ================================================= */}

                            <textarea
                                ref={
                                    messageInputRef
                                }
                                value={
                                    message
                                }
                                onChange={(
                                    event
                                ) => {

                                    setMessage(
                                        event.target.value
                                    );


                                    // Automatically grow
                                    // only when necessary

                                    const textarea =
                                        event.target;

                                    textarea.style.height =
                                        "auto";


                                    const maxHeight =
                                        128;


                                    textarea.style.height =
                                        `${Math.min(
                                            textarea.scrollHeight,
                                            maxHeight
                                        )}px`;

                                }}
                                onKeyDown={(
                                    event
                                ) => {

                                    if (
                                        event.key ===
                                        "Enter" &&
                                        !event.shiftKey
                                    ) {

                                        event.preventDefault();

                                        sendMessage(
                                            event
                                        );

                                    }

                                }}
                                placeholder="
                                    Message MindMirror...
                                "
                                rows={1}
                                disabled={
                                    sending
                                }
                                className="
                                    flex-1
                                    bg-transparent
                                    resize-none
                                    outline-none
                                    overflow-y-auto
                                    px-3
                                    py-3
                                    text-gray-700
                                    placeholder:text-gray-400
                                    max-h-32
                                "
                            />


                            <button
                                type="submit"
                                disabled={
                                    sending ||
                                    !message.trim()
                                }
                                className="
                                    w-11
                                    h-11
                                    rounded-xl
                                    bg-purple-600
                                    text-white
                                    flex
                                    items-center
                                    justify-center
                                    hover:bg-purple-700
                                    disabled:opacity-40
                                    disabled:cursor-not-allowed
                                    transition
                                    flex-shrink-0
                                "
                            >
                                ↑
                            </button>

                        </div>


                        <p className="
                            text-center
                            text-[10px]
                            text-gray-400
                            mt-2
                        ">
                            MindMirror is here to listen,
                            reflect and talk with you.
                        </p>

                    </form>

                </div>

            </main>

        </div>

    );

}


export default Journal;