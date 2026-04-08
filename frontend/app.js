const API = "http://127.0.0.1:8000";

let accessibility = false;
let xp = parseInt(localStorage.getItem("xp")) || 0;

window.onload = () => {
  loadHistory();
  updateXP();
};

// XP
function gainXP(amount) {
  xp += amount;
  localStorage.setItem("xp", xp);
  updateXP();
}

function updateXP() {
  document.getElementById("xp-display").innerText = `XP: ${xp}`;
}

// CHAT
function addMessage(text, type) {
  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  msg.innerText = text;
  document.getElementById("messages").appendChild(msg);
  scrollDown();
}

function typeMessage(text, type) {
  const msg = document.createElement("div");
  msg.className = `message ${type}`;
  document.getElementById("messages").appendChild(msg);

  let i = 0;
  const interval = setInterval(() => {
    msg.innerText += text[i];
    i++;
    if (i >= text.length) clearInterval(interval);
  }, 10);

  scrollDown();
}

function adaptText(text) {
  if (!accessibility) return text;
  return text.replace(/,/g, "\n").replace(/\./g, ".\n\n").toUpperCase();
}

function speak(text) {
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "pt-BR";
  speechSynthesis.speak(u);
}

async function sendQuestion() {

  const input = document.getElementById("question");
  const question = input.value;
  if (!question) return;

  addMessage(question, "user");
  saveMessage(question, "user");

  input.value = "";

  const thinking = document.createElement("div");
  thinking.className = "message bot";
  thinking.innerText = "Pensando...";
  document.getElementById("messages").appendChild(thinking);

  const res = await fetch(`${API}/ask`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      question,
      user_profile: {
        age_group: document.getElementById("age").value,
        level: document.getElementById("level").value
      }
    })
  });

  const data = await res.json();

  thinking.remove();

  let text = adaptText(data.answer);

  typeMessage(text, "bot");
  saveMessage(text, "bot");
  speak(text);

  if (data.paths) {
    let reasoning = "🧠 Como pensei:\n\n";
    data.paths.forEach(p => {
      p.path.forEach(step => {
        reasoning += `${step[0]} → ${step[1]} → ${step[2]}\n`;
      });
    });
    typeMessage(reasoning, "bot");
  }
}

// QUIZ
async function getQuiz() {
  const res = await fetch(`${API}/quiz`);
  const data = await res.json();
  renderQuiz(data);
}

function renderQuiz(data) {
  const container = document.createElement("div");
  container.className = "message bot";

  const q = document.createElement("p");
  q.innerText = `🎯 ${data.question}`;
  container.appendChild(q);

  data.options.forEach(opt => {
    const btn = document.createElement("button");
    btn.innerText = opt;

    btn.onclick = () => {
      if (opt === data.correct) {
        btn.style.background = "#22c55e";
        gainXP(10);
      } else {
        btn.style.background = "#ef4444";
      }
    };

    container.appendChild(btn);
  });

  document.getElementById("messages").appendChild(container);
  scrollDown();
}

// DASHBOARD
async function showDashboard() {

  document.getElementById("chat-view").classList.add("hidden");
  document.getElementById("dashboard-view").classList.remove("hidden");

  const res = await fetch(`${API}/finance/analyze`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      transactions: [
        {category: "lazer", amount: 300},
        {category: "alimentacao", amount: 600}
      ]
    })
  });

  const data = await res.json();

  renderChart(data);

  typeMessage("📊 Insights carregados!", "bot");
}

// MENTOR
async function runMentor() {

  const res = await fetch(`${API}/mentor/analyze`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      income: 5000,
      expenses: [
        {category: "lazer", amount: 300},
        {category: "moradia", amount: 1500}
      ]
    })
  });

  const r = await res.json();

  typeMessage(`
💰 Economia: ${r.monthly_savings}
📅 Ano: ${r.yearly_projection}
🚀 Futuro: ${r.future_5_years}
`, "bot");
}

// UI
function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("collapsed");
}

function toggleMode() {
  document.body.classList.toggle("light");
}

function toggleAccessibility() {
  accessibility = !accessibility;
  typeMessage(accessibility ? "♿ Acessibilidade ON" : "♿ Acessibilidade OFF", "bot");
}

// VOICE
function startVoice() {
  const r = new webkitSpeechRecognition();
  r.lang = "pt-BR";
  r.onresult = e => {
    document.getElementById("question").value = e.results[0][0].transcript;
  };
  r.start();
}