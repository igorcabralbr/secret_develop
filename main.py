from fastapi import FastAPI
from pydantic import BaseModel

# CORE
from core.graph_engine import FinancialGraph
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.quiz_engine import QuizEngine
from core.finance_engine import FinanceEngine
from core.user_engine import UserProfile
from core.accessibility_engine import AccessibilityEngine
from core.brain_orchestrator import FinancialBrain


# -------------------------
# FASTAPI INIT
# -------------------------

app = FastAPI(title="Financial Brain API")


# -------------------------
# REQUEST MODELS
# -------------------------

class QuestionRequest(BaseModel):
    question: str


class UserConfig(BaseModel):
    age_group: str = "adult"        # teen | adult | elderly
    level: str = "iniciante"       # iniciante | intermediario | avancado
    accessibility: str = "normal"  # normal | high_contrast | simple | neurodivergent


# -------------------------
# LOAD ENGINES
# -------------------------

print("🔄 Inicializando Financial Brain...")

graph = FinancialGraph(
    "data/concepts.json",
    "data/relations.json"
)

reasoner = ReasoningEngine(graph)

rag = RAGEngine(graph)

quiz_engine = QuizEngine(
    "data/relations.json",
    "data/concepts.json"
)

# Exemplo de dados financeiros (pode vir do usuário depois)
finance_engine = FinanceEngine([
    {"category": "alimentacao", "amount": 800},
    {"category": "lazer", "amount": 300},
    {"category": "transporte", "amount": 200}
])

# usuário padrão (pode ser dinâmico depois)
user_profile = UserProfile("adult", "iniciante")

accessibility = AccessibilityEngine("normal")

# ORQUESTRADOR
brain = FinancialBrain(
    graph,
    reasoner,
    rag,
    quiz_engine,
    finance_engine,
    user_profile,
    accessibility
)

print("✅ Financial Brain pronto!")


# -------------------------
# ENDPOINTS
# -------------------------

@app.get("/health")
def health():
    return {"status": "ok", "message": "Financial Brain is running"}


# -------------------------
# ASK (principal)
# -------------------------

@app.post("/ask")
def ask(req: QuestionRequest):

    response = brain.handle(req.question)

    return {
        "question": req.question,
        "response": response
    }


# -------------------------
# QUIZ
# -------------------------

@app.get("/quiz")
def get_quiz():

    quiz = quiz_engine.generate_quiz()

    return quiz


# -------------------------
# USER CONFIG (dinâmico)
# -------------------------

@app.post("/user/config")
def configure_user(config: UserConfig):

    global user_profile, accessibility, brain

    user_profile = UserProfile(config.age_group, config.level)
    accessibility = AccessibilityEngine(config.accessibility)

    # recria brain com novo contexto
    brain = FinancialBrain(
        graph,
        reasoner,
        rag,
        quiz_engine,
        finance_engine,
        user_profile,
        accessibility
    )

    return {
        "message": "Configuração atualizada",
        "user": config.dict()
    }