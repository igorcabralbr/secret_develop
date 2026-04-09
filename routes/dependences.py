from core.graph_engine import FinancialGraph
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.quiz_engine import QuizEngine
from core.finance_engine import FinanceEngine
from core.user_engine import UserProfile
from accessibility.accessibility_engine import AccessibilityEngine
from core.decision_engine import DecisionEngine


# 🔥 SINGLETON DO CÉREBRO

graph = FinancialGraph("data/concepts.json", "data/relations.json")

reasoner = ReasoningEngine(graph)
rag = RAGEngine(graph)
quiz = QuizEngine("data/relations.json", "data/concepts.json")

transactions = [
    {"category": "alimentacao", "amount": 800},
    {"category": "lazer", "amount": 350},
    {"category": "transporte", "amount": 200}
]

finance = FinanceEngine(transactions)

user = UserProfile(age_group="adult", level="iniciante")

accessibility = AccessibilityEngine(mode="normal")

decision_engine = DecisionEngine(
    graph,
    reasoner,
    rag,
    quiz,
    finance,
    user,
    accessibility
)