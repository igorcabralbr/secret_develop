from fastapi import APIRouter
from pydantic import BaseModel

from core.graph_engine import FinancialGraph
from core.mentor_engine import MentorEngine
from core.llm_engine import LLMEngine

router = APIRouter()

graph = FinancialGraph("data/concepts.json", "data/relations.json")
mentor_engine = MentorEngine(graph)
llm = LLMEngine()


class MentorRequest(BaseModel):
    income: float
    expenses: list


def build_prompt(data):

    return f"""
Você é um mentor financeiro.

Analise os dados abaixo e dê recomendações claras e práticas.

DADOS:
- renda: {data['income']}
- gastos: {data['expenses']}
- economia mensal: {data['savings']}
- taxa de poupança: {data['savings_rate']}
- categorias: {data['categories']}

INSIGHTS:
{data['insights']}

Dê:
1. Diagnóstico
2. Problemas
3. Sugestões práticas
4. Próximos passos
"""


@router.post("/mentor/analyze")
def mentor(req: MentorRequest):

    analysis = mentor_engine.analyze(
        req.income,
        req.expenses
    )

    prompt = build_prompt(analysis)

    response = llm.generate(prompt)

    return {
        "monthly_savings": analysis["savings"],
        "yearly_projection": analysis["savings"] * 12,
        "future_5_years": analysis["savings"] * 12 * 5,
        "analysis": response
    }