# core/reasoning_engine.py

from typing import List, Dict, Any


class ReasoningEngine:
    def __init__(self, graph_engine):
        self.graph_engine = graph_engine

    # =========================
    # MAIN PROCESS (EVOLUÍDO)
    # =========================
    def process(
        self,
        query: str,
        context: List[Dict],
        user_profile: Dict = None,
    ) -> Dict:

        steps = self._build_reasoning_chain(context)

        return {
            "query": query,
            "steps": steps,
            "confidence": self._calculate_confidence(context),
        }

    # =========================
    # BUILD LOGICAL CHAIN
    # =========================
    def _build_reasoning_chain(self, context: List[Dict]) -> List[Dict]:
        chain = []

        for rel in context:
            chain.append({
                "from": rel.get("source"),
                "to": rel.get("target"),
                "relation": rel.get("type"),
                "effect": rel.get("effect"),
                "strength": rel.get("weight", 0.5),
                "logic": self._infer_logic(rel),
            })

        return chain

    # =========================
    # NOVO: INFERÊNCIA LÓGICA SIMPLES
    # =========================
    def _infer_logic(self, rel: Dict) -> str:
        effect = rel.get("effect", "")

        if "increase" in effect or "sobe" in effect:
            return "positive_correlation"

        if "decrease" in effect or "cai" in effect:
            return "negative_correlation"

        return "neutral_correlation"

    # =========================
    # CONFIDENCE SCORE
    # =========================
    def _calculate_confidence(self, context: List[Dict]) -> float:
        if not context:
            return 0.0

        weights = [r.get("weight", 0.5) for r in context]
        return sum(weights) / len(weights)

    # =========================
    # NOVO: FORMATO PARA LLM
    # =========================
    def prepare_for_llm(self, reasoning: Dict) -> Dict:
        """
        Reduz estrutura para linguagem do LLM
        """

        steps = []

        for s in reasoning["steps"]:
            steps.append(
                f"{s['from']} → {s['to']} ({s['effect']})"
            )

        return {
            "reasoning_steps": steps,
            "confidence": reasoning["confidence"]
        }