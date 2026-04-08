class FinancialBrain:

    def __init__(
        self,
        graph,
        reasoner,
        rag,
        quiz,
        finance,
        user,
        accessibility
    ):
        self.graph = graph
        self.reasoner = reasoner
        self.rag = rag
        self.quiz = quiz
        self.finance = finance
        self.user = user
        self.accessibility = accessibility

    # -------------------------
    # INTERPRETAÇÃO DE INTENÇÃO
    # -------------------------

    def detect_intent(self, question):

        q = question.lower()

        if any(k in q for k in ["gasto", "despesa", "dinheiro"]):
            return "finance"

        if any(k in q for k in ["o que é", "definição", "conceito"]):
            return "education"

        if any(k in q for k in ["quiz", "pergunta"]):
            return "quiz"

        if any(k in q for k in ["impacto", "acontece", "se"]):
            return "reasoning"

        return "unknown"

    # -------------------------
    # ROTEADOR PRINCIPAL
    # -------------------------

    def handle(self, question):

        intent = self.detect_intent(question)

        if intent == "finance":
            return self.handle_finance()

        if intent == "education":
            return self.handle_education(question)

        if intent == "quiz":
            return self.quiz.generate_quiz()

        if intent == "reasoning":
            return self.handle_reasoning(question)

        return "Não entendi sua pergunta ainda."

    # -------------------------
    # EDUCAÇÃO (RAG)
    # -------------------------

    def handle_education(self, question):

        concept = question.replace("o que é", "").strip()

        data = self.rag.explain_concept(concept)

        text = data["definition"]

        return self._finalize(text)

    # -------------------------
    # RACIOCÍNIO
    # -------------------------

    def handle_reasoning(self, question):

        # simplificado: pega primeira palavra relevante
        words = question.split()
        concept = words[-1]

        paths = self.reasoner.find_paths(concept)

        if not paths:
            return "Não encontrei relação suficiente."

        best_path = paths[0]["path"]

        explanation = self._build_explanation(best_path)

        return self._finalize(explanation)

    # -------------------------
    # FINANÇAS PESSOAIS
    # -------------------------

    def handle_finance(self):

        total = self.finance.total_spending()
        by_cat = self.finance.spending_by_category()

        text = f"Você gastou {total}. Distribuição: {by_cat}"

        return self._finalize(text)

    # -------------------------
    # EXPLICAÇÃO DE CAMINHO
    # -------------------------

    def _build_explanation(self, path):

        sentences = []

        for source, rel, target in path:
            sentences.append(f"{source} {rel} {target}")

        return " → ".join(sentences)

    # -------------------------
    # PIPE FINAL (USER + ACCESSIBILITY)
    # -------------------------

    def _finalize(self, text):

        text = self.user.adapt_text(text)

        text = self.accessibility.format_text(text)

        return text