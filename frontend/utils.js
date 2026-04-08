function saveMessage(text, type) {
  let history = JSON.parse(localStorage.getItem("chat")) || [];
  history.push({text, type});
  localStorage.setItem("chat", JSON.stringify(history));
}

function loadHistory() {
  let history = JSON.parse(localStorage.getItem("chat")) || [];
  history.forEach(m => addMessage(m.text, m.type));
}

function scrollDown() {
  const el = document.getElementById("messages");
  el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
}