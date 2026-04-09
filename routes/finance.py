from fastapi import APIRouter
from routes.dependencies import decision_engine

router = APIRouter()


@router.get("/finance")
def get_finance():

    response = decision_engine.handle("me mostre meus gastos")

    return {
        "analysis": response
    }