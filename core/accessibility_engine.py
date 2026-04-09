# core/accessibility_engine.py

from typing import Dict, Any


class AccessibilityEngine:
    def __init__(self):
        pass

    # =========================
    # MAIN ADAPT (EVOLUÍDO)
    # =========================
    def adapt(self, content: Any, user_profile: Dict = None) -> Dict:
        """
        Adapta resposta para o perfil do usuário
        """

        if not user_profile:
            return {
                "content": content,
                "format": "default"
            }

        level = user_profile.get("level", "beginner")
        age_group = user_profile.get("age_group", "adult")
        learning_style = user_profile.get("learning_style", "visual")

        adapted_content = self._adapt_content(content, level, age_group, learning_style)

        return {
            "content": adapted_content,
            "metadata": {
                "level": level,
                "age_group": age_group,
                "learning_style": learning_style
            }
        }

    # =========================
    # CORE ADAPTATION LOGIC
    # =========================
    def _adapt_content(self, content: Any, level: str, age_group: str, learning_style: str):

        # 🔹 se conteúdo vier estruturado (LLM + reasoning)
        if isinstance(content, dict):
            content = content.get("content") or content.get("result") or content

        text = str(content)

        # =========================
        # BEGINNER MODE
        # =========================
        if level == "beginner":
            return self._simplify_text(text, age_group)

        # =========================
        # INTERMEDIATE MODE
        # =========================
        if level == "intermediate":
            return self._balanced_text(text)

        # =========================
        # ADVANCED MODE
        # =========================
        if level == "advanced":
            return self._technical_text(text)

        return text

    # =========================
    # SIMPLIFICATION
    # =========================
    def _simplify_text(self, text: str, age_group: str):

        simplified = f"""
Explicação simples:

{text}

Resumo: foque no conceito principal.
"""

        if age_group == "teen":
            simplified += "\n💡 Pense nisso como algo do dia a dia."

        return simplified

    # =========================
    # BALANCED MODE
    # =========================
    def _balanced_text(self, text: str):
        return f"""
Explicação:

{text}

Se quiser aprofundar, posso detalhar mais.
"""

    # =========================
    # ADVANCED MODE
    # =========================
    def _technical_text(self, text: str):
        return f"""
Análise técnica:

{text}

Inclui relações estruturais do sistema financeiro.
"""

    # =========================
    # NOVO: LLM PRE-FORMATTER
    # =========================
    def format_for_llm(self, content: Any, user_profile: Dict) -> Dict:
        """
        Prepara contexto antes do LLM (caso usado upstream)
        """

        return {
            "content": content,
            "level": user_profile.get("level"),
            "style": user_profile.get("learning_style"),
            "tone": self._get_tone(user_profile)
        }

    # =========================
    # NOVO: TONE CONTROL
    # =========================
    def _get_tone(self, user_profile: Dict) -> str:
        level = user_profile.get("level", "beginner")

        if level == "beginner":
            return "didactic"
        elif level == "intermediate":
            return "explanatory"
        else:
            return "technical"