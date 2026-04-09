# core/brain_orchestrator.py

class BrainOrchestrator:
    def __init__(
        self,
        graph_engine,
        reasoning_engine,
        rag_engine,
        quiz_engine,
        finance_engine,
        user_engine,
        accessibility_engine,
    ):
        self.graph_engine = graph_engine
        self.reasoning_engine = reasoning_engine
        self.rag_engine = rag_engine
        self.quiz_engine = quiz_engine
        self.finance_engine = finance_engine
        self.user_engine = user_engine
        self.accessibility_engine = accessibility_engine

    # =========================
    # 🧠 ENTRY POINT (mantido)
    # =========================
    def process_query(self, query: str, user_id: str = None):
        """
        Método principal (mantido, mas evoluído internamente)
        """

        # 🔹 1. Buscar usuário
        user = self._get_user(user_id)

        # 🔹 2. Detectar intenção
        intent = self._detect_intent(query)

        # 🔹 3. Roteamento inteligente
        raw_response = self._route_by_intent(query, intent, user)

        # 🔹 4. Adaptar resposta (acessibilidade)
        final_response = self._adapt_response(raw_response, user)

        return {
            "intent": intent,
            "response": final_response
        }

    # =========================
    # 🧭 INTENT DETECTION (NOVO)
    # =========================
    def _detect_intent(self, query: str) -> str:
        query_lower = query.lower()

        if any(word in query_lower for word in ["o que é", "definição", "conceito"]):
            return "concept"

        elif any(word in query_lower for word in ["calcular", "quanto rende", "simular"]):
            return "calculation"

        elif any(word in query_lower for word in ["quiz", "teste", "pergunta"]):
            return "quiz"

        elif any(word in query_lower for word in ["explique", "por que", "como funciona"]):
            return "explanation"

        return "general"

    # =========================
    # 🔀 ROUTER (NOVO CORE)
    # =========================
    def _route_by_intent(self, query: str, intent: str, user: dict):

        try:
            # 📚 Conceitos → Graph
            if intent == "concept":
                return self._handle_concept(query)

            # 💰 Cálculo financeiro
            elif intent == "calculation":
                return self._handle_calculation(query, user)

            # 🎮 Quiz
            elif intent == "quiz":
                return self._handle_quiz(query, user)

            # 🧠 Explicação estruturada
            elif intent == "explanation":
                return self._handle_explanation(query, user)

            # 🌐 Fallback (RAG + reasoning)
            else:
                return self._handle_general(query, user)

        except Exception as e:
            return {
                "error": str(e),
                "fallback": self._handle_general(query, user)
            }

    # =========================
    # 📚 HANDLERS
    # =========================

    def _handle_concept(self, query: str):
        concept = self.graph_engine.find_concept(query)
        relations = self.graph_engine.get_related(concept["id"])

        return {
            "type": "concept",
            "concept": concept,
            "relations": relations
        }

    def _handle_calculation(self, query: str, user: dict):
        result = self.finance_engine.compute(query, user_context=user)

        return {
            "type": "calculation",
            "result": result
        }

    def _handle_quiz(self, query: str, user: dict):
        quiz = self.quiz_engine.generate(query, user_profile=user)

        return {
            "type": "quiz",
            "quiz": quiz
        }

    def _handle_explanation(self, query: str, user: dict):
        context = self.graph_engine.search(query)

        reasoning = self.reasoning_engine.process(
            query=query,
            context=context,
            user_profile=user
        )

        return {
            "type": "explanation",
            "content": reasoning
        }

    def _handle_general(self, query: str, user: dict):
        context = self.rag_engine.retrieve(query)

        reasoning = self.reasoning_engine.process(
            query=query,
            context=context,
            user_profile=user
        )

        return {
            "type": "general",
            "content": reasoning
        }

    # =========================
    # 👤 USER HANDLING (NOVO)
    # =========================
    def _get_user(self, user_id: str):
        if not user_id:
            return {"level": "beginner", "age_group": "adult"}

        return self.user_engine.get_user(user_id)

    # =========================
    # ♿ ACCESSIBILITY (AGORA CENTRAL)
    # =========================
    def _adapt_response(self, response: dict, user: dict):
        return self.accessibility_engine.adapt(
            content=response,
            user_profile=user
        )