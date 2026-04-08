from fastapi import APIRouter
from pydantic import BaseModel

from core.graph_engine import FinancialGraph
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.user_engine import UserProfile

router = APIRouter()

# carregar cérebro (singleton simples)
graph = FinancialGraph("data/concepts.json", "data/relations.json")
reasoner = ReasoningEngine(graph)
rag = RAGEngine(graph)


class AskRequest(BaseModel):
    question: str
    user_profile: dict


@router.post("/ask")
def ask(req: AskRequest):

    question = req.question.lower()

    # 🔎 identificar conceito (simples, pode evoluir depois)
    concept = None
    for node in graph.graph.nodes:
        if node in question:
            concept = node
            break

    if not concept:
        concept = list(graph.graph.nodes)[0]

    # 🧠 raciocínio
    paths = reasoner.find_paths(concept, depth=3)

    # 📘 explicação
    explanation = rag.explain_concept(concept)

    # 👤 perfil
    user = UserProfile(
        req.user_profile.get("age_group", "adult"),
        req.user_profile.get("level", "iniciante")
    )

    answer = f"{explanation['definition']}"

    answer = user.adapt_text(answer)

    return {
        "answer": answer,
        "paths": paths[:2]
    }