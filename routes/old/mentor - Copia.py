from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MentorRequest(BaseModel):
    income: float
    expenses: list


@router.post("/mentor/analyze")
def mentor(req: MentorRequest):

    total_expenses = sum(e["amount"] for e in req.expenses)

    monthly_savings = req.income - total_expenses

    yearly = monthly_savings * 12

    future_5y = yearly * 5

    return {
        "monthly_savings": monthly_savings,
        "yearly_projection": yearly,
        "future_5_years": future_5y
    }