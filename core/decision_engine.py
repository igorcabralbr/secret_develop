import re


class DecisionEngine:

    def __init__(
        self,
        graph,
        reasoning_engine,
        rag_engine,
        quiz_engine,
        finance_engine=None,
        user_profile=None,
        accessibility_engine=None
    ):

        self.graph = graph
        self.reasoner = reasoning_engine
        self.rag = rag_engine
        self.quiz = quiz_engine
        self.finance = finance_engine
        self.user = user_profile
        self.accessibility = accessibility_engine

    # -----------------------------
    # ENTRYPOINT PRINCIPAL
    # -----------------------------

    def handle(self, question):

        intent = self.detect_intent(question)
        concept = self.extract_concept(question)

        response = ""

        if intent == "education":
            response = self.handle_education(concept)

        elif intent == "causal":
            response = self.handle_causal(concept)

        elif intent == "finance":
            response = self.handle_finance()

        elif intent == "quiz":
            response = self.handle_quiz()

        else:
            response = "Não entendi sua pergunta. Pode reformular?"

        return self.apply_post_processing(response)

    # -----------------------------
    # INTENT DETECTION
    # -----------------------------

    def detect_intent(self, question):

        q = question.lower()

        if any(x in q for x in ["o que é", "explique", "defina"]):
            return "education"

        if any(x in q for x in ["se", "impacto", "acontece"]):
            return "causal"

        if any(x in q for x in ["gasto", "dinheiro", "posso investir"]):
            return "finance"

        if any(x in q for x in ["quiz", "pergunta", "teste"]):
            return "quiz"

        return "unknown"

    # -----------------------------
    # CONCEPT EXTRACTION
    # -----------------------------

    def extract_concept(self, question):

        words = re.findall(r"\w+", question.lower())

        # tenta achar um conceito existente no grafo
        for w in words:
            if w in self.graph.graph.nodes:
                return w

        return None

    # -----------------------------
    # EDUCAÇÃO (RAG)
    # -----------------------------

    def handle_education(self, concept):

        if not concept:
            return "Não identifiquei o conceito."

        explanation = self.rag.explain_concept(concept)

        return f"{explanation['concept']}: {explanation['definition']}"

    # -----------------------------
    # RACIOCÍNIO CAUSAL
    # -----------------------------

    def handle_causal(self, concept):

        if not concept:
            return "Não identifiquei o conceito para análise."

        paths = self.reasoner.find_paths(concept)

        if not paths:
            return "Não encontrei relações relevantes."

        best_path = paths[0]["path"]

        explanation = []

        for step in best_path:
            explanation.append(f"{step[0]} → {step[1]} → {step[2]}")

        return "Impacto provável:\n" + "\n".join(explanation)

    # -----------------------------
    # FINANÇAS PESSOAIS
    # -----------------------------

    def handle_finance(self):

        if not self.finance:
            return "Dados financeiros não disponíveis."

        total = self.finance.total_spending()
        categories = self.finance.spending_by_category()
        highest = self.finance.highest_category()

        response = f"Gasto total: {total}\n"

        response += "Gastos por categoria:\n"

        for k, v in categories.items():
            response += f"- {k}: {v}\n"

        if highest:
            response += f"\nMaior gasto: {highest}"

        return response

    # -----------------------------
    # QUIZ
    # -----------------------------

    def handle_quiz(self):

        q = self.quiz.generate_quiz()

        text = f"{q['question']}\n"

        for i, opt in enumerate(q["options"]):
            text += f"{chr(65+i)}) {opt}\n"

        return text

    # -----------------------------
    # PÓS-PROCESSAMENTO
    # -----------------------------

    def apply_post_processing(self, text):

        # 1️⃣ adaptação por usuário
        if self.user:
            text = self.user.adapt_text(text)

        # 2️⃣ acessibilidade
        if self.accessibility:
            text = self.accessibility.format_text(text)

        return text