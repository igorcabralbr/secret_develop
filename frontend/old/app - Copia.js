const API_URL = "http://localhost:8000";

// -------------------------
// ELEMENTOS DOM
// -------------------------

const input = document.getElementById("input");
const responseBox = document.getElementById("response");

const ageSelect = document.getElementById("age");
const levelSelect = document.getElementById("level");
const accessibilitySelect = document.getElementById("accessibility");


// -------------------------
// UTIL
// -------------------------

function setLoading(state) {
    if (state) {
        responseBox.innerText = "Pensando...";
    }
}

function showResponse(text) {
    responseBox.innerText = text;
}


// -------------------------
// ASK
// -------------------------

async function sendQuestion() {

    const question = input.value.trim();

    if (!question) {
        showResponse("Digite uma pergunta.");
        return;
    }

    try {

        setLoading(true);

        const res = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await res.json();

        showResponse(data.response);

    } catch (error) {

        console.error(error);
        showResponse("Erro ao conectar com o servidor.");

    }
}


// -------------------------
// QUIZ
// -------------------------

async function getQuiz() {

    try {

        setLoading(true);

        const res = await fetch(`${API_URL}/quiz`);
        const data = await res.json();

        renderQuiz(data);

    } catch (error) {

        console.error(error);
        showResponse("Erro ao carregar quiz.");

    }
}


// -------------------------
// RENDER QUIZ
// -------------------------

function renderQuiz(quiz) {

    const container = document.getElementById("quiz");

    container.innerHTML = "";

    const question = document.createElement("p");
    question.innerText = quiz.question;

    container.appendChild(question);

    quiz.options.forEach(option => {

        const btn = document.createElement("button");

        btn.innerText = option;

        btn.onclick = () => checkAnswer(option, quiz.correct);

        container.appendChild(btn);
    });
}


// -------------------------
// CHECK ANSWER
// -------------------------

function checkAnswer(selected, correct) {

    if (selected === correct) {
        showResponse("✅ Resposta correta!");
    } else {
        showResponse(`❌ Errado! Resposta correta: ${correct}`);
    }
}


// -------------------------
// CONFIG USER
// -------------------------

async function updateUserConfig() {

    const config = {
        age_group: ageSelect.value,
        level: levelSelect.value,
        accessibility: accessibilitySelect.value
    };

    try {

        const res = await fetch(`${API_URL}/user/config`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(config)
        });

        const data = await res.json();

        showResponse("Configuração atualizada!");

    } catch (error) {

        console.error(error);
        showResponse("Erro ao atualizar usuário.");

    }
}


// -------------------------
// ENTER PARA ENVIAR
// -------------------------

input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendQuestion();
    }
});