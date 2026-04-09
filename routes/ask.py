from fastapi import APIRouter
from pydantic import BaseModel
from routes.dependencies import decision_engine

router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(req: AskRequest):

    response = decision_engine.handle(req.question)

    return {
        "question": req.question,
        "response": response
    }