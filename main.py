# main.py

from fastapi import FastAPI
from pydantic import BaseModel

print("START") #J
# =========================
# IMPORTS DOS ENGINES
# =========================
from core.graph_engine import GraphEngine
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.quiz_engine import QuizEngine
from core.finance_engine import FinanceEngine
from core.user_engine import UserEngine
from core.accessibility_engine import AccessibilityEngine
from core.llm_engine import LLMEngine
from core.brain_orchestrator import BrainOrchestrator




# =========================
# APP
# =========================
app = FastAPI(title="Financial Brain API")


# =========================
# REQUEST MODEL
# =========================
class AskRequest(BaseModel):
    query: str
    user_id: str | None = None


# =========================
# INIT ENGINES (mantido + evoluído)
# =========================

# 🔹 Base de conhecimento
graph_engine = GraphEngine(
    concepts_path="data/concepts.json",
    relations_path="data/relations.json"
)

# 🔹 RAG
rag_engine = RAGEngine(graph_engine=graph_engine)

# 🔹 Reasoning (agora usa graph)
reasoning_engine = ReasoningEngine(graph_engine=graph_engine)

# 🔹 LLM (NOVO)
#llm_engine = LLMEngine(provider="openai", model="gpt-4o-mini")
llm_engine = LLMEngine(provider="mock")

# 🔹 Outros módulos
#quiz_engine = QuizEngine(graph_engine=graph_engine, llm_engine)
quiz_engine = QuizEngine(graph_engine, llm_engine)
finance_engine = FinanceEngine()
user_engine = UserEngine()
accessibility_engine = AccessibilityEngine()


# =========================
# ORCHESTRATOR (NOVO CORE)
# =========================
brain = BrainOrchestrator(
    graph_engine=graph_engine,
    reasoning_engine=reasoning_engine,
    rag_engine=rag_engine,
    quiz_engine=quiz_engine,
    finance_engine=finance_engine,
    user_engine=user_engine,
    accessibility_engine=accessibility_engine,
    llm_engine=llm_engine,  # 🔥 integração LLM
)



# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"status": "Financial Brain running"}


# =========================
# ENDPOINT PRINCIPAL
# =========================
@app.post("/ask")
def ask(request: AskRequest):
    """
    Endpoint principal do sistema cognitivo
    """

    result = brain.process_query(
        query=request.query,
        user_id=request.user_id
    )

    return result


# =========================
# ENDPOINT OPCIONAL (DEBUG)
# =========================
@app.post("/debug/reasoning")
def debug_reasoning(request: AskRequest):
    """
    Retorna o raciocínio estruturado (sem LLM)
    """

    context = rag_engine.retrieve(request.query)

    reasoning = reasoning_engine.process(
        query=request.query,
        context=context,
        user_profile=None
    )

    return reasoning


# =========================
# ENDPOINT OPCIONAL (LLM DIRETO)
# =========================
@app.post("/debug/llm")
def debug_llm(request: AskRequest):
    """
    Teste direto do LLM (sem orquestrador)
    """

    response = llm_engine.generate(prompt=request.query)

    return {"response": response}


if __name__ == "__main__":
    print("START")

    while True:
        query = input("Digite sua pergunta: ")

        if query.lower() in ["exit", "sair"]:
            break

        result = brain.process_query(query, user_id="test")

        print(result)