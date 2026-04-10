const API_URL = "http://127.0.0.1:8000/ask"; // ajuste se necessário

// elementos do DOM (mantém seus IDs originais se já existirem)
const chatContainer = document.getElementById("chat-container");
const inputField = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

// ==============================
// formata mensagem 
// ==============================
function formatMessage(text) {
    if (!text) return "";

    return text
        // remove espaços extras à esquerda
        .replace(/\n\s+/g, "\n")
        
        // transforma quebras de linha em <br>
        .replace(/\n/g, "<br>")
        
        // destaque títulos simples
        .replace(/💡 (.*?)<br>/g, "<strong>💡 $1</strong><br><br>")
        .replace(/Resumo:/g, "<strong>Resumo:</strong>")
        .replace(/Exemplo:/g, "<strong>Exemplo:</strong>")
        .replace(/Em termos simples:/g, "<strong>Em termos simples:</strong>");
}

// ==============================
// 🧠 UTIL: cria mensagem visual
// ==============================
function createMessage(text, sender = "bot") {
    const message = document.createElement("div");
    message.classList.add("message", sender);

    // 🔥 GARANTE QUE SEMPRE É STRING
    if (typeof text === "object") {
        message.textContent = JSON.stringify(text, null, 2);
    } else {
//        message.textContent = text;
		message.innerHTML = formatMessage(text);
    }

    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ==============================
// ⏳ LOADING MESSAGE
// ==============================
function createLoadingMessage() {
    const message = document.createElement("div");
    message.classList.add("message", "bot", "loading");
    message.innerText = "Thinking...";
    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return message;
}

// ==============================
// 🔄 PARSE FLEXÍVEL DA RESPOSTA
// ==============================

function extractResponse(data) {
    if (!data) return "No response from server.";

    // string direta
    if (typeof data === "string") return data;

    // 🧠 NOVO: seu formato real
    if (data.response && data.response.content) {
        return data.response.content;
    }

    // fallback comum
    if (typeof data.answer === "string") return data.answer;
    if (typeof data.response === "string") return data.response;
    if (typeof data.message === "string") return data.message;

    // fallback final
    return JSON.stringify(data, null, 2);
}


// ==============================
// 🚀 ENVIO PARA BACKEND
// ==============================
async function sendMessage() {
    const userText = inputField.value.trim();

    if (!userText) return;

    createMessage(userText, "user");
    inputField.value = "";

    const loadingMessage = createLoadingMessage();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: userText
            })
        });

        const data = await response.json();

        loadingMessage.remove();

        const botText = extractResponse(data);
        createMessage(botText, "bot");

    } catch (error) {
        loadingMessage.remove();
        createMessage("Erro ao conectar com o backend.", "bot");
        console.error(error);
    }
}

// ==============================
// 🎯 EVENTOS
// ==============================
sendButton.addEventListener("click", sendMessage);

inputField.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});