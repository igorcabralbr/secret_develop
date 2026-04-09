# routes/ask.py

from fastapi import APIRouter
from pydantic import BaseModel

# 🔹 IMPORT DO ORCHESTRATOR (NOVO)
from core.brain_orchestrator import BrainOrchestrator

# 🔹 IMPORT DOS ENGINES (mantido, mas organizado)
from core.graph_engine import GraphEngine
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.quiz_engine import QuizEngine
from core.finance_engine import FinanceEngine
from core.user_engine import UserEngine
from core.accessibility_engine import AccessibilityEngine
from core.llm_engine import LLMEngine


router = APIRouter()


# =========================
# REQUEST MODEL (mantido)
# =========================
class AskRequest(BaseModel):
    query: str
    user_id: str | None = None


# =========================
# INIT ENGINES (AGORA CENTRALIZADO AQUI)
# =========================

# 🔹 Base de conhecimento
graph_engine = GraphEngine(
    concepts_path="data/concepts.json",
    relations_path="data/relations.json"
)

# 🔹 RAG
rag_engine = RAGEngine(graph_engine=graph_engine)

# 🔹 Reasoning
reasoning_engine = ReasoningEngine(graph_engine=graph_engine)

# 🔹 Outros módulos
quiz_engine = QuizEngine(graph_engine=graph_engine)
finance_engine = FinanceEngine()
user_engine = UserEngine()
accessibility_engine = AccessibilityEngine()

# 🔹 LLM (NOVO)
llm_engine = LLMEngine(
    provider="openai",  # pode trocar pra "mock"
    model="gpt-4o-mini"
)

# =========================
# ORCHESTRATOR (CORE REAL)
# =========================
brain = BrainOrchestrator(
    graph_engine=graph_engine,
    reasoning_engine=reasoning_engine,
    rag_engine=rag_engine,
    quiz_engine=quiz_engine,
    finance_engine=finance_engine,
    user_engine=user_engine,
    accessibility_engine=accessibility_engine,
    llm_engine=llm_engine,
)


# =========================
# ENDPOINT PRINCIPAL
# =========================
@router.post("/ask")
def ask(request: AskRequest):
    """
    Endpoint cognitivo principal
    """

    result = brain.process_query(
        query=request.query,
        user_id=request.user_id
    )

    return result


# =========================
# DEBUG (NÃO REMOVE — SÓ ADICIONA)
# =========================

@router.post("/ask/debug/reasoning")
def debug_reasoning(request: AskRequest):
    """
    Debug do raciocínio (sem LLM)
    """

    context = rag_engine.retrieve(request.query)

    reasoning = reasoning_engine.process(
        query=request.query,
        context=context,
        user_profile=None
    )

    return reasoning


@router.post("/ask/debug/llm")
def debug_llm(request: AskRequest):
    """
    Debug direto do LLM
    """

    response = llm_engine.generate(
        prompt=request.query
    )

    return {"response": response}