# core/llm_engine.py

import os
from typing import Optional, Any, Dict


class LLMEngine:
    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini"):
        self.provider = provider
        self.model = model
        self.client = None
        self._init_client()

    # =========================
    # INIT
    # =========================
    def _init_client(self):
        if self.provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except Exception:
                self.client = None

        elif self.provider == "mock":
            self.client = None

    # =========================
    # MAIN GENERATE
    # =========================
    def generate(
        self,
        prompt: str,
        context: Optional[Any] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 500,
    ) -> str:

        full_prompt = self._build_prompt(prompt, context, system_prompt)

        if self.provider == "openai" and self.client:
            return self._generate_openai(full_prompt, temperature, max_tokens)

        return self._mock_response(full_prompt)

    # =========================
    # PROMPT BUILDER (ANTI-ALUCINAÇÃO)
    # =========================
    def _build_prompt(self, prompt, context, system_prompt):

        base_system = system_prompt or """
Você é um assistente de educação financeira.

REGRAS IMPORTANTES:
- Use APENAS o contexto fornecido
- NÃO invente relações
- NÃO adicione informações externas
- Se não souber, diga claramente
- Explique de forma didática
"""

        context_block = ""
        if context:
            context_block = f"\n\nDADOS ESTRUTURADOS:\n{context}"

        return f"""
{base_system}

PERGUNTA:
{prompt}

{context_block}

Explique com base nos dados acima.
"""

    # =========================
    # OPENAI
    # =========================
    def _generate_openai(self, prompt, temperature, max_tokens):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Assistente financeiro estruturado"},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Erro LLM: {str(e)}]"

    # =========================
    # MOCK (fallback)
    # =========================
    def _mock_response(self, prompt):
        return f"[LLM MOCK]\n{prompt[:200]}..."

    # =========================
    # MÉTODO PRINCIPAL DE EXPLICAÇÃO
    # =========================
    def explain_from_reasoning(
        self,
        query: str,
        reasoning_data: Dict,
        user_profile: Dict,
    ) -> str:

        return self.generate(
            prompt=query,
            context=reasoning_data,
            system_prompt=f"""
Você é um professor de educação financeira.

Adapte para:
- nível: {user_profile.get("level", "beginner")}
- público: {user_profile.get("age_group", "adult")}

Explique passo a passo com base nos dados estruturados.
"""
        )