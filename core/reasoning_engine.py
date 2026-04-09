# core/reasoning_engine.py

from typing import List, Dict, Any


class ReasoningEngine:
    def __init__(self, graph_engine):
        self.graph_engine = graph_engine

    # =========================
    # PROCESS (mantido, mas evoluído)
    # =========================
    def process(
        self,
        query: str,
        context: List[Dict],
        user_profile: Dict = None,
    ) -> Dict:
        """
        Agora retorna RACIOCÍNIO ESTRUTURADO (não texto)
        """

        steps = self._build_reasoning_steps(context)

        return {
            "query": query,
            "steps": steps,
            "confidence": self._estimate_confidence(context),
        }

    # =========================
    # BUILD REASONING
    # =========================
    def _build_reasoning_steps(self, context: List[Dict]) -> List[Dict]:
        steps = []

        for relation in context:
            step = {
                "from": relation.get("source"),
                "to": relation.get("target"),
                "type": relation.get("type"),
                "effect": relation.get("effect"),
                "strength": relation.get("weight", 0.5),
            }
            steps.append(step)

        return steps

    # =========================
    # CONFIDENCE
    # =========================
    def _estimate_confidence(self, context: List[Dict]) -> float:
        if not context:
            return 0.0

        weights = [r.get("weight", 0.5) for r in context]
        return sum(weights) / len(weights)

    # =========================
    # NOVO: PREPARAR PARA LLM
    # =========================
    def prepare_for_llm(self, reasoning_output: Dict) -> Dict:
        """
        Converte para formato amigável ao LLM
        """

        steps_text = []

        for step in reasoning_output["steps"]:
            steps_text.append(
                f"{step['from']} → {step['to']} ({step['effect']})"
            )

        return {
            "steps": steps_text,
            "confidence": reasoning_output["confidence"]
        }