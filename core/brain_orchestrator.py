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
        llm_engine=None,  # 🔥 NOVO (não quebra código antigo)
    ):
        self.graph_engine = graph_engine
        self.reasoning_engine = reasoning_engine
        self.rag_engine = rag_engine
        self.quiz_engine = quiz_engine
        self.finance_engine = finance_engine
        self.user_engine = user_engine
        self.accessibility_engine = accessibility_engine

        # 🔥 fallback seguro
        self.llm_engine = llm_engine

    # =========================
    # MAIN ENTRY
    # =========================
    def process_query(self, query: str, user_id: str = None):

        try:
            # =========================
            # USER SAFE
            # =========================
            user_context = {}
            user_profile = {}

            if user_id:
                try:
                    user_context = self.user_engine.get_context(user_id) or {}
                    user_profile = user_context.get("profile", {}) or {}
                except Exception:
                    pass

            # =========================
            # INTENT
            # =========================
            intent = self._detect_intent(query)

            # =========================
            # ROUTE
            # =========================
            try:
                raw_response = self._route(query, intent, user_profile)
            except Exception as e:
                raw_response = {
                    "type": "error",
                    "message": f"Erro no roteamento: {str(e)}"
                }

            # =========================
            # ACCESSIBILITY
            # =========================
            try:
                final_response = self.accessibility_engine.adapt(
                    content=raw_response,
                    user_profile=user_profile
                )
            except Exception:
                final_response = raw_response

            return {
                "intent": intent,
                "response": final_response
            }

        except Exception as e:
            return {
                "intent": "error",
                "response": f"Erro geral: {str(e)}"
            }

    # =========================
    # ROUTER
    # =========================
    def _route(self, query: str, intent: str, user_profile: dict):

        if intent == "concept":
            return self._handle_concept(query)

        if intent == "calculation":
            return self._handle_calculation(query, user_profile)

        if intent == "quiz":
            return self._handle_quiz(query, user_profile)

        if intent == "explanation":
            return self._handle_explanation(query, user_profile)

        return self._handle_general(query, user_profile)

    # =========================
    # CONCEPT
    # =========================
#    def _handle_concept(self, query: str):
#
#        try:
#            concept = self.graph_engine.find_concept(query)
#        except Exception:
#            concept = {}
#
#        concept_id = concept.get("id") if concept else None
#
#        try:
#            relations = self.graph_engine.get_related(concept_id) if concept_id else []
#        except Exception:
#            relations = []
#
#        return {
#            "type": "concept",
#            "concept": concept,
#            "relations": relations
#        }

    def _handle_concept(self, query: str):

        try:
            concept = self.graph_engine.find_concept(query)
        except Exception:
            concept = {}

        concept_id = concept.get("id") if concept else None

        try:
            relations = self.graph_engine.get_related(concept_id) if concept_id else []
        except Exception:
            relations = []

        # 🔥 NOVO: limitar relações (evita poluição)
        relations_limited = relations[:3] if relations else []

        # 🔥 NOVO: montar contexto para LLM
        llm_context = {
            "concept": concept,
            "relations": relations_limited
        }

        # 🔥 NOVO: geração com LLM (mock ou real)
        try:
            explanation = self.llm_engine.generate(
                prompt=query,
                context=llm_context,
                system_prompt="Explique de forma simples, didática e clara."
            ) if self.llm_engine else str(concept)
        except Exception:
            explanation = str(concept)

        # 🔥 IMPORTANTE: mantém compatibilidade + adiciona resposta bonita
        return {
            "type": "concept",
            "concept": concept,
            "relations": relations,
            "content": explanation  # 👈 NOVO (isso resolve seu problema)
        }

    # =========================
    # 💰 CALCULATION (NOVO FLOW)
    # =========================
    def _handle_calculation(self, query: str, user_profile: dict):

        try:
            computation = self.finance_engine.compute(query, user_context=user_profile)
        except Exception as e:
            return {"error": f"Erro no cálculo: {str(e)}"}

        try:
            explanation = self.finance_engine.explain_with_llm(
                query=query,
                computation=computation,
                user_context=user_profile or {}
            )
        except Exception:
            explanation = str(computation)

        return {
            "type": "calculation",
            "computation": computation,
            "explanation": explanation
        }

    # =========================
    # QUIZ
    # =========================
    def _handle_quiz(self, query: str, user_profile: dict):

        try:
            return self.quiz_engine.generate(query, user_context=user_profile)
        except Exception as e:
            return {"error": f"Erro no quiz: {str(e)}"}

    # =========================
    # EXPLANATION
    # =========================
    def _handle_explanation(self, query: str, user_profile: dict):

        try:
            context = self.rag_engine.retrieve(query)
        except Exception:
            context = []

        if not context:
            return {
                "type": "fallback",
                "content": "Não encontrei dados suficientes."
            }

        try:
            reasoning = self.reasoning_engine.process(
                query=query,
                context=context,
                user_profile=user_profile
            )
        except Exception:
            reasoning = {}

        try:
            llm_context = self.reasoning_engine.prepare_for_llm(reasoning)
        except Exception:
            llm_context = reasoning

        try:
            explanation = self.llm_engine.explain_from_reasoning(
                query=query,
                reasoning_data=llm_context,
                user_profile=user_profile or {}
            ) if self.llm_engine else str(reasoning)
        except Exception:
            explanation = str(reasoning)

        return {
            "type": "explanation",
            "content": explanation
        }

    # =========================
    # GENERAL
    # =========================
    def _handle_general(self, query: str, user_profile: dict):

        try:
            context = self.rag_engine.retrieve(query)
        except Exception:
            context = []

        try:
            reasoning = self.reasoning_engine.process(
                query=query,
                context=context,
                user_profile=user_profile
            )
        except Exception:
            reasoning = {}

        try:
            llm_context = self.reasoning_engine.prepare_for_llm(reasoning)
        except Exception:
            llm_context = reasoning

        try:
            response = self.llm_engine.explain_from_reasoning(
                query=query,
                reasoning_data=llm_context,
                user_profile=user_profile or {}
            ) if self.llm_engine else str(reasoning)
        except Exception:
            response = str(reasoning)

        return {
            "type": "general",
            "content": response
        }

    # =========================
    # INTENT
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