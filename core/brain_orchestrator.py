# =========================
# IMPORTS ORIGINAIS (mantidos)
# =========================
# (mantenha todos os seus imports aqui)

# =========================
# NOVO: CONTRATO UNIVERSAL
# =========================
def _default_response():
    return {
        "type": "answer",
        "content": "",
        "confidence": 0.0,
        "source": "unknown",
        "metadata": {}
    }


# =========================
# NOVO: ADAPTERS (não quebram nada)
# =========================
def _adapt_graph_output(raw):
    try:
        return {
            "type": "explanation",
            "content": raw.get("content", str(raw)),
            "confidence": raw.get("confidence", 0.6),
            "source": "graph",
            "metadata": raw
        }
    except:
        return _default_response()


def _adapt_rag_output(raw):
    try:
        return {
            "type": "context",
            "content": raw.get("content", str(raw)),
            "confidence": raw.get("confidence", 0.7),
            "source": "rag",
            "metadata": raw
        }
    except:
        return _default_response()


def _adapt_reasoning_output(raw):
    try:
        return {
            "type": "reasoning",
            "content": raw.get("content", str(raw)),
            "confidence": raw.get("confidence", 0.8),
            "source": "reasoning",
            "metadata": raw
        }
    except:
        return _default_response()


def _adapt_quiz_output(raw):
    return {
        "type": "quiz",
        "content": raw,
        "confidence": 1.0,
        "source": "quiz",
        "metadata": {}
    }


# =========================
# NOVO: DETECÇÃO DE INTENÇÃO (simples e robusta)
# =========================
def _detect_intent(user_input: str):
    text = user_input.lower()

    if "quiz" in text or "pergunta" in text or "teste" in text:
        return "quiz"

    if "explica" in text or "o que é" in text:
        return "explanation"

    return "general"


# =========================
# NOVO: LLM WRAPPER (plugável)
# =========================
class LLMClient:
    def __init__(self):
        # você pode conectar OpenAI aqui depois
        pass

    def generate(self, question, context=None, reasoning=None):
        # fallback simples (não quebra se não tiver LLM real)
        response = f"Pergunta: {question}\n"

        if context:
            response += f"\nContexto:\n{context}\n"

        if reasoning:
            response += f"\nRaciocínio:\n{reasoning}\n"

        response += "\nResposta gerada (modo fallback)."

        return {
            "content": response,
            "confidence": 0.75
        }


# =========================
# NOVO: ORCHESTRATOR CORE
# =========================
class BrainOrchestrator:

    def __init__(
        self,
        graph_engine=None,
        rag_engine=None,
        reasoning_engine=None,
        quiz_engine=None,
        finance_engine=None,
        user_engine=None,
        accessibility_engine=None,
        llm_client=None
    ):
        # mantém compatibilidade total
        self.graph_engine = graph_engine
        self.rag_engine = rag_engine
        self.reasoning_engine = reasoning_engine
        self.quiz_engine = quiz_engine
        self.finance_engine = finance_engine
        self.user_engine = user_engine
        self.accessibility_engine = accessibility_engine

        self.llm = llm_client or LLMClient()

    # =========================
    # PIPELINE PRINCIPAL
    # =========================
    def process(self, user_input: str):

        intent = _detect_intent(user_input)

        # =========================
        # QUIZ FLOW (isolado)
        # =========================
        if intent == "quiz" and self.quiz_engine:
            raw_quiz = self._safe_call(self.quiz_engine, "run", user_input)
            return _adapt_quiz_output(raw_quiz)

        # =========================
        # RAG
        # =========================
        rag_data = None
        if self.rag_engine:
            raw_rag = self._safe_call(self.rag_engine, "retrieve", user_input)
            rag_data = _adapt_rag_output(raw_rag)

        # =========================
        # REASONING
        # =========================
        reasoning_data = None
        if self.reasoning_engine:
            raw_reasoning = self._safe_call(
                self.reasoning_engine,
                "think",
                user_input,
                rag_data
            )
            reasoning_data = _adapt_reasoning_output(raw_reasoning)

        # =========================
        # GRAPH (opcional, enriquece)
        # =========================
        graph_data = None
        if self.graph_engine:
            raw_graph = self._safe_call(self.graph_engine, "query", user_input)
            graph_data = _adapt_graph_output(raw_graph)

        # =========================
        # LLM FINAL
        # =========================
        final = self.llm.generate(
            question=user_input,
            context=self._merge_contexts(rag_data, graph_data),
            reasoning=reasoning_data["content"] if reasoning_data else None
        )

        return {
            "type": "answer",
            "content": final["content"],
            "confidence": final.get("confidence", 0.7),
            "source": "llm",
            "metadata": {
                "rag": rag_data,
                "reasoning": reasoning_data,
                "graph": graph_data
            }
        }

    # =========================
    # HELPERS (robustez)
    # =========================
    def _safe_call(self, engine, method_name, *args):
        try:
            method = getattr(engine, method_name, None)

            if callable(method):
                return method(*args)

            # fallback para engines diferentes
            if callable(engine):
                return engine(*args)

            return None

        except Exception as e:
            return {
                "error": str(e)
            }

    def _merge_contexts(self, rag, graph):
        parts = []

        if rag and rag.get("content"):
            parts.append(rag["content"])

        if graph and graph.get("content"):
            parts.append(graph["content"])

        return "\n\n".join(parts)