from fastapi import APIRouter
from core.quiz_engine import QuizEngine

router = APIRouter()

quiz_engine = QuizEngine(
    "data/relations.json",
    "data/concepts.json"
)

@router.get("/quiz")
def get_quiz():

    return quiz_engine.generate_quiz()