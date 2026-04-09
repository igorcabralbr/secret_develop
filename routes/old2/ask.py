from fastapi import APIRouter
from pydantic import BaseModel

from core.graph_engine import FinancialGraph
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.user_engine import UserProfile
from core.llm_engine import LLMEngine

router = APIRouter()

graph = FinancialGraph("data/concepts.json", "data/relations.json")
reasoner = ReasoningEngine(graph)
rag = RAGEngine(graph)
llm = LLMEngine()


class AskRequest(BaseModel):
    question: str
    user_profile: dict


def extract_concept(question, graph):

    q = question.lower()

    for node in graph.graph.nodes:
        if node in q:
            return node

    return None


def build_context(concept, rag, paths):

    explanation = rag.explain_concept(concept)

    reasoning_text = ""

    for p in paths[:3]:
        for step in p["path"]:
            reasoning_text += f"{step[0]} -> {step[1]} -> {step[2]}\n"

    context = f"""
CONCEITO:
{explanation['concept']}

DEFINIÇÃO:
{explanation['definition']}

RACIOCÍNIO FINANCEIRO:
{reasoning_text}
"""

    return context


def build_prompt(question, context, user_profile):

    return f"""
Responda a pergunta do usuário usando APENAS o contexto abaixo.

Seja claro, didático e correto financeiramente.

Adapte para:
- idade: {user_profile.get("age_group")}
- nível: {user_profile.get("level")}

Pergunta:
{question}

Contexto:
{context}
"""


@router.post("/ask")
def ask(req: AskRequest):

    question = req.question

    concept = extract_concept(question, graph)

    if not concept:
        concept = list(graph.graph.nodes)[0]

    # 🧠 reasoning
    paths = reasoner.find_paths(concept, depth=3)

    # 📚 contexto (RAG + grafo)
    context = build_context(concept, rag, paths)

    # 🤖 prompt
    prompt = build_prompt(question, context, req.user_profile)

    # 🔥 LLM
    answer = llm.generate(prompt)

    # 👤 adaptação final
    user = UserProfile(
        req.user_profile.get("age_group", "adult"),
        req.user_profile.get("level", "iniciante")
    )

    answer = user.adapt_text(answer)

    return {
        "answer": answer,
        "paths": paths[:2]
    }