from fastapi import APIRouter
from pydantic import BaseModel
from routes.dependencies import decision_engine

router = APIRouter()


class UserUpdate(BaseModel):
    age_group: str
    level: str


@router.post("/user")
def update_user(data: UserUpdate):

    decision_engine.user.age_group = data.age_group
    decision_engine.user.level = data.level

    return {
        "message": "Perfil atualizado",
        "profile": {
            "age_group": data.age_group,
            "level": data.level
        }
    }