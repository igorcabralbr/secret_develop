from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.ask import router as ask_router
from routes.quiz import router as quiz_router
from routes.finance import router as finance_router
from routes.mentor import router as mentor_router

app = FastAPI()

# CORS (ESSENCIAL para frontend funcionar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas
app.include_router(ask_router)
app.include_router(quiz_router)
app.include_router(finance_router)
app.include_router(mentor_router)


@app.get("/")
def root():
    return {"status": "Financial Brain API rodando"}