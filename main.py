from core.graph_engine import FinancialGraph
from core.reasoning_engine import ReasoningEngine
from core.rag_engine import RAGEngine
from core.quiz_engine import QuizEngine
from core.finance_engine import FinanceEngine
from core.user_engine import UserProfile
from accessibility.accessibility_engine import AccessibilityEngine
from core.decision_engine import DecisionEngine


# ---------------------------------------
# 1️⃣ CARREGAR FINANCIAL BRAIN
# ---------------------------------------

graph = FinancialGraph(
    "data/concepts.json",
    "data/relations.json"
)

reasoner = ReasoningEngine(graph)
rag = RAGEngine(graph)
quiz = QuizEngine(
    "data/relations.json",
    "data/concepts.json"
)


# ---------------------------------------
# 2️⃣ DADOS DO USUÁRIO (SIMULAÇÃO)
# ---------------------------------------

transactions = [
    {"category": "alimentacao", "amount": 800},
    {"category": "lazer", "amount": 350},
    {"category": "transporte", "amount": 200},
    {"category": "assinaturas", "amount": 100}
]

finance = FinanceEngine(transactions)


# ---------------------------------------
# 3️⃣ PERFIL DO USUÁRIO
# ---------------------------------------

user = UserProfile(
    age_group="adult",        # teen | adult | elderly
    level="iniciante"         # iniciante | intermediario | avancado
)


# ---------------------------------------
# 4️⃣ ACESSIBILIDADE
# ---------------------------------------

accessibility = AccessibilityEngine(
    mode="simple"  # normal | simple | high_contrast | neurodivergent
)


# ---------------------------------------
# 5️⃣ DECISION ENGINE (CÉREBRO CENTRAL)
# ---------------------------------------

engine = DecisionEngine(
    graph=graph,
    reasoning_engine=reasoner,
    rag_engine=rag,
    quiz_engine=quiz,
    finance_engine=finance,
    user_profile=user,
    accessibility_engine=accessibility
)


# ---------------------------------------
# 6️⃣ LOOP INTERATIVO (CLI)
# ---------------------------------------

def run_cli():

    print("\n🧠 Financial Brain iniciado!")
    print("Digite sua pergunta ou 'sair' para encerrar.\n")

    while True:

        question = input("Você: ")

        if question.lower() in ["sair", "exit", "quit"]:
            print("Encerrando Financial Brain...")
            break

        response = engine.handle(question)

        print("\nBrain:", response)
        print("\n" + "-"*50 + "\n")


# ---------------------------------------
# 7️⃣ EXEMPLOS AUTOMÁTICOS (DEBUG)
# ---------------------------------------

def run_examples():

    examples = [

        "o que é inflacao",
        "se inflacao aumentar o que acontece",
        "me mostre meus gastos",
        "quero um quiz"
    ]

    for q in examples:

        print(f"\nPergunta: {q}")
        print("Resposta:")
        print(engine.handle(q))
        print("\n" + "="*60)


# ---------------------------------------
# 8️⃣ ENTRYPOINT
# ---------------------------------------

if __name__ == "__main__":

    # escolha o modo:
    mode = "cli"  # "cli" ou "test"

    if mode == "cli":
        run_cli()

    else:
        run_examples()