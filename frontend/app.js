// ==========================================
// CONFIG
// ==========================================

const API_BASE = "http://localhost:8000";

// ==========================================
// UTIL: NORMALIZAR RESPOSTA (🔥 NOVO)
// ==========================================

function getResponseData(data) {
    return data.response || data.answer || "Resposta não encontrada.";
}

// ==========================================
// ENVIO DE PERGUNTA
// ==========================================

async function sendQuestion() {

    const input = document.getElementById("user-input");
    const output = document.getElementById("chat-output");

    const question = input.value;

    if (!question) return;

    appendMessage("Você", question);

    try {

        const res = await fetch(`${API_BASE}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await res.json();

        const responseText = getResponseData(data);

        appendMessage("Brain", responseText);

    } catch (err) {

        appendMessage("Erro", "Erro ao conectar com o servidor.");
        console.error(err);
    }

    input.value = "";
}

// ==========================================
// QUIZ
// ==========================================

async function loadQuiz() {

    try {

        const res = await fetch(`${API_BASE}/quiz`);
        const data = await res.json();

        const quizText = getResponseData(data.quiz || data);

        appendMessage("Quiz", quizText);

    } catch (err) {

        appendMessage("Erro", "Erro ao carregar quiz.");
        console.error(err);
    }
}

// ==========================================
// FINANCE
// ==========================================

async function loadFinance() {

    try {

        const res = await fetch(`${API_BASE}/finance`);
        const data = await res.json();

        const financeText = getResponseData(data.analysis || data);

        appendMessage("Finance", financeText);

    } catch (err) {

        appendMessage("Erro", "Erro ao carregar dados financeiros.");
        console.error(err);
    }
}

// ==========================================
// EXPLAIN
// ==========================================

async function explainConcept(concept) {

    try {

        const res = await fetch(`${API_BASE}/explain/${concept}`);
        const data = await res.json();

        const text = getResponseData(data.explanation || data);

        appendMessage("Explicação", text);

    } catch (err) {

        appendMessage("Erro", "Erro ao explicar conceito.");
        console.error(err);
    }
}

// ==========================================
// USER PROFILE
// ==========================================

async function updateUserProfile(age_group, level) {

    try {

        const res = await fetch(`${API_BASE}/user`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ age_group, level })
        });

        const data = await res.json();

        appendMessage("Sistema", "Perfil atualizado com sucesso.");

    } catch (err) {

        appendMessage("Erro", "Erro ao atualizar perfil.");
        console.error(err);
    }
}

// ==========================================
// UI HELPERS
// ==========================================

function appendMessage(sender, message) {

    const output = document.getElementById("chat-output");

    const div = document.createElement("div");
    div.classList.add("message");

    div.innerHTML = `<strong>${sender}:</strong> ${message}`;

    output.appendChild(div);

    output.scrollTop = output.scrollHeight;
}

// ==========================================
// EVENT LISTENERS (mantido)
// ==========================================

document.getElementById("send-btn").addEventListener("click", sendQuestion);

document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendQuestion();
    }
});

// ==========================================
// BOTÕES EXTRAS (se existirem)
// ==========================================

const quizBtn = document.getElementById("quiz-btn");
if (quizBtn) {
    quizBtn.addEventListener("click", loadQuiz);
}

const financeBtn = document.getElementById("finance-btn");
if (financeBtn) {
    financeBtn.addEventListener("click", loadFinance);
}