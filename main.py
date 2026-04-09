# =========================================
# IMPORTS EXISTENTES (mantidos)
# =========================================

from core.graph_engine import FinancialGraph
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.quiz_engine import QuizEngine
from core.finance_engine import FinanceEngine
from core.user_engine import UserProfile
from accessibility.accessibility_engine import AccessibilityEngine
from core.decision_engine import DecisionEngine

# 🔥 NOVO IMPORT (CRÍTICO)
from routes.dependencies import decision_engine as shared_engine


# =========================================
# NOVO: FASTAPI
# =========================================

from fastapi import FastAPI
from routes.ask import router as ask_router
from routes.quiz import router as quiz_router
from routes.finance import router as finance_router
from routes.user import router as user_router
from routes.explain import router as explain_router


# =========================================
# 1️⃣ FINANCIAL BRAIN (mantido)
# =========================================

graph = FinancialGraph(
    "data/concepts.json",
    "data/relations.json"
)

reasoner = ReasoningEngine(graph)
rag = RAGEngine(graph)

quiz = QuizEngine(
    "data/relations.json",
    "data/concepts.json"
)


# =========================================
# 2️⃣ DADOS DO USUÁRIO (mantido)
# =========================================

transactions = [
    {"category": "alimentacao", "amount": 800},
    {"category": "lazer", "amount": 350},
    {"category": "transporte", "amount": 200},
    {"category": "assinaturas", "amount": 100}
]

finance = FinanceEngine(transactions)


# =========================================
# 3️⃣ PERFIL DO USUÁRIO (mantido)
# =========================================

user = UserProfile(
    age_group="adult",
    level="iniciante"
)


# =========================================
# 4️⃣ ACESSIBILIDADE (mantido)
# =========================================

accessibility = AccessibilityEngine(
    mode="simple"
)


# =========================================
# 5️⃣ DECISION ENGINE (AJUSTADO)
# =========================================

# ⚠️ ANTES você criava outro engine aqui
# AGORA usamos o compartilhado

engine = shared_engine  # 🔥 AGORA EXISTE APENAS UM CÉREBRO


# =========================================
# 6️⃣ CLI (mantido)
# =========================================

def run_cli():

    print("\n🧠 Financial Brain iniciado!")
    print("Digite sua pergunta ou 'sair' para encerrar.\n")

    while True:

        question = input("Você: ")

        if question.lower() in ["sair", "exit", "quit"]:
            print("Encerrando Financial Brain...")
            break

        response = engine.handle(question)

        print("\nBrain:", response)
        print("\n" + "-"*50 + "\n")


# =========================================
# 7️⃣ TESTES (mantido)
# =========================================

def run_examples():

    examples = [

        "o que é inflacao",
        "se inflacao aumentar o que acontece",
        "me mostre meus gastos",
        "quero um quiz"
    ]

    for q in examples:

        print(f"\nPergunta: {q}")
        print("Resposta:")
        print(engine.handle(q))
        print("\n" + "="*60)


# =========================================
# 8️⃣ FASTAPI APP (mantido)
# =========================================

app = FastAPI(title="Financial Brain API")

app.include_router(ask_router)
app.include_router(quiz_router)
app.include_router(finance_router)
app.include_router(user_router)
app.include_router(explain_router)


# =========================================
# 9️⃣ ENTRYPOINT (mantido)
# =========================================

if __name__ == "__main__":

    mode = "cli"  # "cli", "test", "api"

    if mode == "cli":
        run_cli()

    elif mode == "test":
        run_examples()

    elif mode == "api":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)