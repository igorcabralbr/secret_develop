# core/finance_engine.py

from typing import Dict, Any, Optional
import math


class FinanceEngine:
    def __init__(self, llm_engine=None):
        self.llm_engine = llm_engine

    # =========================
    # MAIN COMPUTE (EVOLUÍDO)
    # =========================
    def compute(self, query: str, user_context: Optional[Dict] = None) -> Dict:

        parsed = self._parse_query(query)

        result = self._execute_calculation(parsed)

        explanation_data = self._build_explanation_context(parsed, result, user_context)

        return {
            "type": "finance",
            "input": parsed,
            "result": result,
            "context": explanation_data
        }

    # =========================
    # PARSER SIMPLES (EXPANSÍVEL)
    # =========================
    def _parse_query(self, query: str) -> Dict:

        q = query.lower()

        if "juros compostos" in q:
            return {
                "type": "compound_interest",
                "principal": self._extract_number(q, default=1000),
                "rate": 0.01,
                "time": 12
            }

        if "juros simples" in q:
            return {
                "type": "simple_interest",
                "principal": self._extract_number(q, default=1000),
                "rate": 0.01,
                "time": 12
            }

        return {
            "type": "unknown",
            "raw": query
        }

    # =========================
    # EXECUÇÃO MATEMÁTICA
    # =========================
    def _execute_calculation(self, data: Dict) -> Dict:

        if data["type"] == "compound_interest":

            p = data["principal"]
            r = data["rate"]
            t = data["time"]

            amount = p * ((1 + r) ** t)

            return {
                "final_amount": round(amount, 2),
                "interest_gained": round(amount - p, 2)
            }

        if data["type"] == "simple_interest":

            p = data["principal"]
            r = data["rate"]
            t = data["time"]

            interest = p * r * t

            return {
                "final_amount": round(p + interest, 2),
                "interest_gained": round(interest, 2)
            }

        return {"message": "No calculation available"}

    # =========================
    # CONTEXTO PARA LLM (NOVO)
    # =========================
    def _build_explanation_context(
        self,
        parsed: Dict,
        result: Dict,
        user_context: Optional[Dict]
    ) -> Dict:

        return {
            "calculation_type": parsed.get("type"),
            "inputs": parsed,
            "result": result,
            "user_level": user_context.get("level") if user_context else "beginner"
        }

    # =========================
    # EXTRAÇÃO DE NÚMEROS
    # =========================
    def _extract_number(self, text: str, default: float = 1000) -> float:

        numbers = []

        for word in text.split():
            try:
                numbers.append(float(word))
            except:
                pass

        return numbers[0] if numbers else default

    # =========================
    # 🤖 LLM EXPLANATION (NOVO)
    # =========================
    def explain_with_llm(
        self,
        query: str,
        computation: Dict,
        user_context: Dict
    ) -> str:

        if not self.llm_engine:
            return self._fallback_explanation(computation)

        return self.llm_engine.generate(
            prompt=query,
            context=computation,
            system_prompt=f"""
Você é um professor de educação financeira.

Explique o resultado do cálculo de forma clara.

Nível do usuário: {user_context.get('level', 'beginner') if user_context else 'beginner'}

IMPORTANTE:
- Não altere os valores
- Explique passo a passo
- Use exemplos simples
"""
        )

    # =========================
    # FALLBACK
    # =========================
    def _fallback_explanation(self, computation: Dict) -> str:
        return f"Resultado do cálculo: {computation}"