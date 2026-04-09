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
        llm_engine,
    ):
        self.graph_engine = graph_engine
        self.reasoning_engine = reasoning_engine
        self.rag_engine = rag_engine
        self.quiz_engine = quiz_engine
        self.finance_engine = finance_engine
        self.user_engine = user_engine
        self.accessibility_engine = accessibility_engine
        self.llm_engine = llm_engine

    # =========================
    # MAIN ENTRY
    # =========================
    def process_query(self, query: str, user_id: str = None):

        user_context = self.user_engine.get_context(user_id) if user_id else None
        user_profile = self.user_engine.get_llm_profile(user_id) if user_id else None

        intent = self._detect_intent(query)

        raw_response = self._route(query, intent, user_context)

        final_response = self.accessibility_engine.adapt(
            content=raw_response,
            user_profile=user_context
        )

        return {
            "intent": intent,
            "response": final_response
        }

    # =========================
    # ROUTER
    # =========================
    def _route(self, query: str, intent: str, user_context: dict):

        if intent == "concept":
            return self._handle_concept(query)

        if intent == "calculation":
            return self._handle_calculation(query, user_context)

        if intent == "quiz":
            return self._handle_quiz(query, user_context)

        if intent == "explanation":
            return self._handle_explanation(query, user_context)

        return self._handle_general(query, user_context)

    # =========================
    # CONCEPT
    # =========================
    def _handle_concept(self, query: str):

        concept = self.graph_engine.find_concept(query)
        relations = self.graph_engine.get_related(concept.get("id"))

        return {
            "type": "concept",
            "concept": concept,
            "relations": relations
        }

    # =========================
    # CALCULATION (UPDATED FINANCE FLOW)
    # =========================
    def _handle_calculation(self, query: str, user_context: dict):

        # 💰 STEP 1: compute deterministic result
        computation = self.finance_engine.compute(query, user_context=user_context)

        # 🧠 STEP 2 (OPTIONAL): reasoning sobre impacto
        reasoning = self.reasoning_engine.process(
            query=query,
            context=[{
                "source": "finance",
                "target": computation.get("input", {}).get("type"),
                "type": "calculation",
                "effect": "financial_result",
                "weight": 1.0
            }],
            user_profile=user_context
        )

        # 🤖 STEP 3: LLM explanation (NOVO FLUXO)
        explanation = self.finance_engine.explain_with_llm(
            query=query,
            computation=computation,
            user_context=user_context or {}
        )

        return {
            "type": "calculation",
            "computation": computation,
            "reasoning": reasoning,
            "explanation": explanation
        }

    # =========================
    # QUIZ
    # =========================
    def _handle_quiz(self, query: str, user_context: dict):

        return self.quiz_engine.generate(query, user_context=user_context)

    # =========================
    # EXPLANATION (RAG + REASONING + LLM)
    # =========================
    def _handle_explanation(self, query: str, user_context: dict):

        context = self.rag_engine.retrieve(query)

        reasoning = self.reasoning_engine.process(
            query=query,
            context=context,
            user_profile=user_context
        )

        llm_context = self.reasoning_engine.prepare_for_llm(reasoning)

        explanation = self.llm_engine.explain_from_reasoning(
            query=query,
            reasoning_data=llm_context,
            user_profile=user_context or {}
        )

        return {
            "type": "explanation",
            "reasoning": reasoning,
            "content": explanation
        }

    # =========================
    # GENERAL
    # =========================
    def _handle_general(self, query: str, user_context: dict):

        context = self.rag_engine.retrieve(query)

        reasoning = self.reasoning_engine.process(
            query=query,
            context=context,
            user_profile=user_context
        )

        llm_context = self.reasoning_engine.prepare_for_llm(reasoning)

        response = self.llm_engine.explain_from_reasoning(
            query=query,
            reasoning_data=llm_context,
            user_profile=user_context or {}
        )

        return {
            "type": "general",
            "content": response
        }

    # =========================
    # INTENT DETECTION (mantido)
    # =========================
    def _detect_intent(self, query: str) -> str:

        q = query.lower()

        if any(x in q for x in ["o que é", "definição"]):
            return "concept"

        if any(x in q for x in ["quanto", "calcular", "juros"]):
            return "calculation"

        if "quiz" in q:
            return "quiz"

        if any(x in q for x in ["por que", "explique", "como funciona"]):
            return "explanation"

        return "general"