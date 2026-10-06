from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ============================================================
# MOOD HISTORY
# ============================================================

mood_history = []


# ============================================================
# CHATBOT RESPONSE
# ============================================================

def generate_response(message):

    text = message.lower()

    if any(word in text for word in
           ["sad", "sadness", "unhappy", "lonely"]):

        return (
            "I'm sorry you're feeling this way. 💙 "
            "You don't have to handle everything alone. "
            "Try talking to someone you trust and give yourself "
            "some time to rest."
        )

    if any(word in text for word in
           ["stress", "stressed", "pressure", "exam"]):

        return (
            "It sounds like you're under a lot of pressure. 🌿 "
            "Try taking a short break, drinking some water, "
            "and dividing your work into smaller tasks."
        )

    if any(word in text for word in
           ["anxiety", "anxious", "nervous", "worry", "worried"]):

        return (
            "Feeling anxious can be difficult. 🌱 "
            "Try taking slow breaths and focusing on one thing "
            "at a time. Talking to someone you trust may also help."
        )

    if any(word in text for word
           in ["angry", "anger", "frustrated", "frustration"]):

        return (
            "It sounds like something is frustrating you. "
            "Give yourself some space before reacting. "
            "A short walk or quiet time may help you feel calmer."
        )

    if any(word in text for word
           in ["happy", "good", "great", "excited"]):

        return (
            "That's wonderful to hear! 😊 "
            "Keep doing things that make you feel positive "
            "and connected."
        )

    if any(word in text for word
           in ["hello", "hi", "hey"]):

        return (
            "Hi! 👋 I'm your Mental Wellness Support Assistant. "
            "You can tell me how you're feeling or what's bothering you."
        )

        # PMS / PERIOD / FOOD
    if any(word in text for word in [
        "pms", "period", "periods", "menstrual", "menstruation"
    ]):
        if any(word in text for word in [
            "food", "eat", "eating", "diet", "healthy"
        ]):
            return (
                "During PMS, you can try healthy foods like bananas, "
                "oranges, leafy vegetables, oats, eggs, curd or yogurt, "
                "nuts, seeds, and whole grains. Drink enough water and "
                "try to limit foods that make your symptoms worse."
            )

        return (
            "PMS can cause cramps, tiredness, bloating, mood changes, "
            "and food cravings. Getting enough sleep, staying hydrated, "
            "eating balanced meals, and doing gentle exercise may help."
        )


    # SLEEP
    if any(word in text for word in [
        "sleep", "sleeping", "insomnia", "can't sleep", "cannot sleep"
    ]):
        return (
            "Good sleep is important for your mental and physical wellbeing. "
            "Try keeping a regular sleep schedule, reducing screen time "
            "before bed, and keeping your room comfortable and quiet."
        )


    # WATER
    if any(word in text for word in [
        "water", "hydration", "dehydrated", "thirsty"
    ]):
        return (
            "Staying hydrated is important. Drink water regularly "
            "throughout the day, especially when you are active or "
            "the weather is hot."
        )


    # EXERCISE
    if any(word in text for word in [
        "exercise", "workout", "gym", "walking", "fitness"
    ]):
        return (
            "Regular physical activity can support both physical and "
            "mental wellbeing. You can try walking, stretching, yoga, "
            "or another activity that feels comfortable for you."
        )


    # HEALTHY FOOD
    if any(word in text for word in [
        "healthy food", "healthy foods", "nutrition", "nutritious"
    ]):
        return (
            "Some nutritious choices include fruits, vegetables, "
            "whole grains, eggs, beans, lentils, nuts, seeds, and "
            "dairy or suitable alternatives. A balanced variety "
            "is better than focusing on only one food."
        )


    # GENERAL HELP
    if any(word in text for word in [
        "help me", "need help", "support me"
    ]):
        return (
            "Of course. 💙 Tell me what you're dealing with, "
            "and I'll try my best to support you."
        )


    # DEFAULT RESPONSE
    return (
        "I hear you. 💙 Tell me a little more about what you're "
        "experiencing, and I'll try to understand and support you."
    )


# ============================================================
# HTML + CSS + JAVASCRIPT
# ============================================================

HTML = """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>MindCare - AI Mental Wellness</title>


<style>

/* ============================================================
   GENERAL
============================================================ */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {

    font-family: Arial, Helvetica, sans-serif;

    background: #f7f9fc;

    color: #243044;

    line-height: 1.6;
}


/* ============================================================
   HEADER
============================================================ */

header {

    width: 100%;

    padding: 18px 8%;

    display: flex;

    justify-content: space-between;

    align-items: center;

    background: white;

    position: sticky;

    top: 0;

    z-index: 1000;

    box-shadow: 0 2px 15px rgba(0,0,0,0.05);
}


.logo {

    font-size: 24px;

    font-weight: bold;

    color: #3563e9;
}


nav {

    display: flex;

    gap: 30px;
}


nav a {

    text-decoration: none;

    color: #526174;

    font-weight: 600;
}


nav a:hover {

    color: #3563e9;
}


/* ============================================================
   HERO
============================================================ */

.hero {

    min-height: 90vh;

    padding: 80px 8%;

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 50px;

    background:
    linear-gradient(
        135deg,
        #eef4ff,
        #f8fbff
    );
}


.hero-text {

    max-width: 650px;
}


.tag {

    display: inline-block;

    padding: 8px 16px;

    border-radius: 30px;

    background: #dfe9ff;

    color: #3563e9;

    font-weight: bold;

    font-size: 14px;
}


.hero h1 {

    font-size: 55px;

    line-height: 1.15;

    margin: 25px 0;
}


.hero h1 span {

    display: block;

    color: #3563e9;
}


.hero p {

    font-size: 18px;

    color: #68768a;

    margin-bottom: 30px;
}


.primary-btn {

    display: inline-block;

    text-decoration: none;

    background: #3563e9;

    color: white;

    padding: 14px 25px;

    border-radius: 10px;

    font-weight: bold;

    transition: 0.3s;
}


.primary-btn:hover {

    transform: translateY(-3px);
}


/* ============================================================
   HERO CARD
============================================================ */

.hero-card {

    width: 340px;

    padding: 45px 35px;

    background: white;

    border-radius: 25px;

    text-align: center;

    box-shadow:
    0 20px 50px rgba(40,70,120,0.15);
}


.heart {

    width: 90px;

    height: 90px;

    margin: auto;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #e9f0ff;

    border-radius: 50%;

    font-size: 42px;
}


.hero-card h3 {

    margin-top: 25px;

    font-size: 23px;
}


.hero-card p {

    color: #718096;

    margin: 12px 0;
}


.mini-status {

    margin-top: 20px;

    color: #4b6075;

    font-size: 14px;
}


.mini-status span {

    display: inline-block;

    width: 9px;

    height: 9px;

    background: #38b87c;

    border-radius: 50%;

    margin-right: 7px;
}


/* ============================================================
   SECTIONS
============================================================ */

.section {

    padding: 90px 8%;
}


.section-title {

    text-align: center;

    max-width: 650px;

    margin: auto auto 45px;
}


.section-title span {

    color: #3563e9;

    font-size: 13px;

    font-weight: bold;

    letter-spacing: 2px;
}


.section-title h2 {

    font-size: 38px;

    margin: 10px 0;
}


.section-title p {

    color: #718096;
}


/* ============================================================
   CHAT
============================================================ */

.chat-container {

    max-width: 850px;

    margin: auto;

    background: white;

    border-radius: 20px;

    overflow: hidden;

    box-shadow:
    0 10px 40px rgba(30,50,80,0.1);
}


.chat-box {

    height: 430px;

    overflow-y: auto;

    padding: 30px;

    background: #f8faff;
}


.message {

    display: flex;

    gap: 12px;

    margin-bottom: 20px;
}


.message.user {

    justify-content: flex-end;
}


.avatar {

    width: 40px;

    height: 40px;

    background: #e1eaff;

    border-radius: 50%;

    display: flex;

    justify-content: center;

    align-items: center;
}


.bubble {

    max-width: 70%;

    padding: 13px 17px;

    border-radius: 15px;

    background: white;

    box-shadow:
    0 3px 10px rgba(0,0,0,0.05);

    word-wrap: break-word;
}


.message.user .bubble {

    background: #3563e9;

    color: white;

    border-radius:
    15px 15px 3px 15px;
}


.typing-area {

    padding: 20px;

    display: flex;

    gap: 10px;

    border-top:
    1px solid #edf0f5;
}


.typing-area input {

    flex: 1;

    padding: 14px;

    border:
    1px solid #dce2eb;

    border-radius: 10px;

    outline: none;

    font-size: 15px;
}


.typing-area input:focus {

    border-color: #3563e9;
}


.typing-area button {

    border: none;

    background: #3563e9;

    color: white;

    padding: 0 25px;

    border-radius: 10px;

    cursor: pointer;

    font-weight: bold;
}


.typing-area button:hover {

    background: #274dcc;
}


/* ============================================================
   MOOD
============================================================ */

.mood-section {

    background: #eef4ff;
}


.mood-grid {

    max-width: 850px;

    margin: auto;

    display: grid;

    grid-template-columns:
    repeat(5, 1fr);

    gap: 15px;
}


.mood-grid button {

    border: none;

    background: white;

    padding: 25px 10px;

    border-radius: 15px;

    cursor: pointer;

    font-size: 15px;

    color: #435168;

    box-shadow:
    0 5px 20px rgba(30,50,80,0.07);

    transition: 0.2s;
}


.mood-grid button:hover {

    transform: translateY(-5px);
}


.mood-grid strong {

    display: block;

    font-size: 35px;

    margin-bottom: 8px;
}


.mood-message {

    text-align: center;

    margin-top: 25px;

    color: #3563e9;

    font-weight: bold;
}


/* ============================================================
   WELLNESS
============================================================ */

.wellness-grid {

    max-width: 1100px;

    margin: auto;

    display: grid;

    grid-template-columns:
    repeat(4, 1fr);

    gap: 20px;
}


.wellness-card {

    background: white;

    padding: 30px 25px;

    border-radius: 18px;

    box-shadow:
    0 8px 30px rgba(30,50,80,0.08);
}


.wellness-card .icon {

    font-size: 38px;
}


.wellness-card h3 {

    margin: 15px 0 8px;
}


.wellness-card p {

    color: #718096;

    font-size: 14px;
}


/* ============================================================
   SAFETY
============================================================ */

.safety {

    margin:
    0 8% 70px;

    padding: 30px;

    border-radius: 15px;

    background: #fff8e8;

    border-left:
    5px solid #f0b429;
}


.safety h3 {

    margin-bottom: 8px;
}


.safety p {

    color: #665b43;
}


/* ============================================================
   FOOTER
============================================================ */

footer {

    text-align: center;

    padding: 45px 20px;

    background: #17233b;

    color: white;
}


footer p {

    color: #b9c4d5;

    margin-top: 5px;
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 900px) {

    .hero {

        flex-direction: column;

        text-align: center;
    }

    .hero h1 {

        font-size: 42px;
    }

    .wellness-grid {

        grid-template-columns:
        repeat(2, 1fr);
    }

    .mood-grid {

        grid-template-columns:
        repeat(3, 1fr);
    }
}


@media (max-width: 600px) {

    nav {

        display: none;
    }

    .hero {

        padding: 60px 5%;
    }

    .hero-card {

        width: 100%;
    }

    .section {

        padding: 60px 5%;
    }

    .wellness-grid {

        grid-template-columns: 1fr;
    }

    .mood-grid {

        grid-template-columns:
        repeat(2, 1fr);
    }

    .typing-area {

        flex-direction: column;
    }

    .typing-area button {

        padding: 14px;
    }

    .bubble {

        max-width: 85%;
    }
}


/* ============================================================
   LOADING
============================================================ */

.loading {

    opacity: 0.6;

    font-style: italic;
}

</style>

</head>


<body>


<!-- =========================================================
     HEADER
========================================================= -->

<header>

    <div class="logo">
        🧠 MindCare
    </div>

    <nav>

        <a href="#home">Home</a>

        <a href="#chat">Chat</a>

        <a href="#mood">Mood</a>

        <a href="#wellness">Wellness</a>

    </nav>

</header>


<!-- =========================================================
     HERO SECTION
========================================================= -->

<section id="home" class="hero">

    <div class="hero-text">

        <span class="tag">
            AI Mental Wellness Support
        </span>

        <h1>

            Your feelings matter.

            <span>
                We're here to listen.
            </span>

        </h1>

        <p>

            MindCare is a supportive AI chatbot
            designed to help you express your
            feelings, understand your emotions,
            and discover simple wellness activities.

        </p>

        <a href="#chat"
           class="primary-btn">

            Start a Conversation 💬

        </a>

    </div>


    <div class="hero-card">

        <div class="heart">
            💙
        </div>

        <h3>
            A safe space to talk
        </h3>

        <p>

            Share what's on your mind
            without judgment.

        </p>

        <div class="mini-status">

            <span></span>

            Assistant is available

        </div>

    </div>

</section>


<!-- =========================================================
     CHAT SECTION
========================================================= -->

<section id="chat"
         class="section">

    <div class="section-title">

        <span>
            AI SUPPORT
        </span>

        <h2>
            Talk to MindCare
        </h2>

        <p>
            Tell me what's on your mind.
        </p>

    </div>


    <div class="chat-container">

        <div id="chatBox"
             class="chat-box">

            <div class="message bot">

                <div class="avatar">
                    🧠
                </div>

                <div class="bubble">

                    Hi! 👋 I'm MindCare.

                    <br><br>

                    You can tell me how you're
                    feeling, what's worrying you,
                    or simply say hello.

                </div>

            </div>

        </div>


        <div class="typing-area">

            <input
                type="text"
                id="messageInput"
                placeholder="Type how you're feeling..."
                autocomplete="off"
            >

            <button
                type="button"
                onclick="sendMessage()">

                Send ➤

            </button>

        </div>

    </div>

</section>


<!-- =========================================================
     MOOD TRACKER
========================================================= -->

<section id="mood"
         class="section mood-section">

    <div class="section-title">

        <span>
            MOOD TRACKER
        </span>

        <h2>
            How are you feeling today?
        </h2>

        <p>

            Tracking your mood can help
            you understand your emotional
            patterns.

        </p>

    </div>


    <div class="mood-grid">

        <button onclick="saveMood('😊 Happy')">

            <strong>😊</strong>

            Happy

        </button>


        <button onclick="saveMood('😌 Calm')">

            <strong>😌</strong>

            Calm

        </button>


        <button onclick="saveMood('😐 Okay')">

            <strong>😐</strong>

            Okay

        </button>


        <button onclick="saveMood('😟 Anxious')">

            <strong>😟</strong>

            Anxious

        </button>


        <button onclick="saveMood('😢 Sad')">

            <strong>😢</strong>

            Sad

        </button>

    </div>


    <p id="moodMessage"
       class="mood-message">
    </p>

</section>


<!-- =========================================================
     WELLNESS SECTION
========================================================= -->

<section id="wellness"
         class="section">

    <div class="section-title">

        <span>
            WELLNESS
        </span>

        <h2>
            Take care of your mind 🌿
        </h2>

        <p>
            Small habits can make a positive difference.
        </p>

    </div>


    <div class="wellness-grid">

        <div class="wellness-card">

            <div class="icon">
                🌬️
            </div>

            <h3>
                Deep Breathing
            </h3>

            <p>

                Take a slow breath in for
                4 seconds and slowly
                breathe out.

            </p>

        </div>


        <div class="wellness-card">

            <div class="icon">
                📝
            </div>

            <h3>
                Journaling
            </h3>

            <p>

                Write down what you're feeling.
                Putting thoughts into words can
                make them easier to understand.

            </p>

        </div>


        <div class="wellness-card">

            <div class="icon">
                🚶
            </div>

            <h3>
                Take a Break
            </h3>

            <p>

                Step away from your screen,
                stretch, walk around, or spend
                some quiet time.

            </p>

        </div>


        <div class="wellness-card">

            <div class="icon">
                🤝
            </div>

            <h3>
                Connect
            </h3>

            <p>

                Talk to a trusted friend,
                family member, teacher,
                or counselor when you need support.

            </p>

        </div>

    </div>

</section>


<!-- =========================================================
     SAFETY
========================================================= -->

<section class="safety">

    <h3>
        💙 Important
    </h3>

    <p>

        MindCare provides general emotional
        wellness support. It is not a replacement
        for a qualified mental-health professional.
        If you need additional support, consider
        talking to a trusted adult, counselor,
        or qualified professional.

    </p>

</section>


<!-- =========================================================
     FOOTER
========================================================= -->

<footer>

    <h3>
        🧠 MindCare
    </h3>

    <p>
        AI-Based Mental Wellness Support Chatbot
    </p>

    <p>
        © 2026 MindCare
    </p>

</footer>


<!-- =========================================================
     JAVASCRIPT
========================================================= -->

<script>


// ============================================================
// SEND CHAT MESSAGE
// ============================================================

async function sendMessage() {

    const input =
        document.getElementById("messageInput");

    const message =
        input.value.trim();


    // Don't send empty messages

    if (message === "") {

        return;

    }


    // Display user's message

    addMessage(
        message,
        "user"
    );


    // Clear input

    input.value = "";


    // Create loading message

    const loading =
        document.createElement("div");


    loading.className =
        "message bot";


    loading.innerHTML = `

        <div class="avatar">
            🧠
        </div>

        <div class="bubble loading">
            Thinking...
        </div>

    `;


    const chatBox =
        document.getElementById("chatBox");


    chatBox.appendChild(
        loading
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;


    try {

        // ====================================================
        // FETCH REQUEST
        // ====================================================

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body:
                    JSON.stringify({
                        message: message
                    })
                }
            );


        // Check server response

        if (!response.ok) {

            throw new Error(
                "Server error: " +
                response.status
            );

        }


        const data =
            await response.json();


        // Remove Thinking...

        loading.remove();


        // Display chatbot response

        addMessage(
            data.response,
            "bot"
        );

    }


    catch (error) {

        console.error(
            "Chat error:",
            error
        );


        loading.remove();


        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    }

}


// ============================================================
// ADD MESSAGE TO CHAT BOX
// ============================================================

function addMessage(
    text,
    sender
) {

    const chatBox =
        document.getElementById("chatBox");


    const messageDiv =
        document.createElement("div");


    if (sender === "user") {

        messageDiv.className =
            "message user";


        messageDiv.innerHTML = `

            <div class="bubble">
                ${text}
            </div>

        `;

    }


    else {

        messageDiv.className =
            "message bot";


        messageDiv.innerHTML = `

            <div class="avatar">
                🧠
            </div>

            <div class="bubble">
                ${text}
            </div>

        `;

    }


    chatBox.appendChild(
        messageDiv
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;

}


// ============================================================
// SAVE MOOD
// ============================================================

async function saveMood(
    mood
) {

    try {

        const response =
            await fetch(
                "/mood",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body:
                    JSON.stringify({
                        mood: mood
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Mood save failed"
            );

        }


        const data =
            await response.json();


        document.getElementById(
            "moodMessage"
        ).innerText =

            data.message +
            " Your mood: " +
            mood;

    }


    catch (error) {

        console.error(
            "Mood error:",
            error
        );


        document.getElementById(
            "moodMessage"
        ).innerText =
            "Unable to save mood.";

    }

}


// ============================================================
// ENTER KEY TO SEND MESSAGE
// ============================================================

document
    .getElementById("messageInput")
    .addEventListener(
        "keypress",
        function(event) {

            if (
                event.key === "Enter"
            ) {

                sendMessage();

            }

        }
    );

</script>


</body>

</html>

"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HTML
    )


# ============================================================
# CHAT API
# ============================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json()


    if not data:

        return jsonify({

            "response":
            "Please type something so I can listen. 💙"

        })


    message = data.get(
        "message",
        ""
    ).strip()


    if not message:

        return jsonify({

            "response":
            "Please type something so I can listen. 💙"

        })


    print(
        "Received message:",
        message
    )


    response = generate_response(message)


    return jsonify({

        "response":
        response

    })


# ============================================================
# MOOD API
# ============================================================

@app.route(
    "/mood",
    methods=["POST"]
)
def save_mood():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
            "Unable to save mood."

        }), 400


    mood = data.get(
        "mood",
        ""
    )


    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )


    mood_history.append({

        "mood":
        mood,

        "date":
        date

    })


    print(
        "Mood saved:",
        mood
    )


    return jsonify({

        "message":
        "Mood saved successfully! 💙",

        "history":
        mood_history

    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )