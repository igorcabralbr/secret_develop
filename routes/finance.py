from fastapi import APIRouter
from pydantic import BaseModel

from core.finance_engine import FinanceEngine

router = APIRouter()


class FinanceRequest(BaseModel):
    transactions: list


@router.post("/finance/analyze")
def analyze(req: FinanceRequest):

    engine = FinanceEngine(req.transactions)

    total = engine.total_spending()
    categories = engine.spending_by_category()
    top = engine.highest_category()

    return {
        "total": total,
        "categories": categories,
        "top_category": top
    }