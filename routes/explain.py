from fastapi import APIRouter
from routes.dependencies import decision_engine

router = APIRouter()


@router.get("/explain/{concept}")
def explain(concept: str):

    response = decision_engine.handle(f"o que é {concept}")

    return {
        "concept": concept,
        "explanation": response
    }