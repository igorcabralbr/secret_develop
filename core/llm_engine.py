# core/llm_engine.py

import os


class LLMEngine:
    def __init__(self, provider="mock"):
        self.provider = provider
        self.api_key = os.getenv("OPENAI_API_KEY")

    # =========================
    # MAIN GENERATE
    # =========================
    def generate(self, prompt: str, context=None, system_prompt=None):

        # =========================
        # MOCK MODE (🔥 PRINCIPAL)
        # =========================
        if self.provider == "mock":
            return self._mock_response(prompt, context)

        # =========================
        # REAL MODE (OPENAI)
        # =========================
        try:
            return self._real_generate(prompt, context, system_prompt)
        except Exception:
            # 🔥 fallback inteligente
            return self._fallback_response(context)

    # =========================
    # MOCK RESPONSE (INTELIGENTE)
    # =========================
    def _mock_response(self, prompt: str, context):

        try:
            if isinstance(context, dict):

                # 🎯 CONCEPT MODE
                if "concept" in context:
                    concept = context.get("concept", {})
                    name = concept.get("name", "conceito")
                    definition = concept.get("definition", "")

                    return f"""
{name.capitalize()} é o aumento geral dos preços ao longo do tempo.

Em termos simples:
Quando a inflação sobe, o dinheiro perde poder de compra — ou seja, você consegue comprar menos com o mesmo valor.

Exemplo:
Se um produto custava R$10 e passa a custar R$12, houve inflação.

Resumo:
Inflação reduz o valor do dinheiro ao longo do tempo.
"""

                # 🎯 FINANCE MODE
                if "result" in context:
                    result = context.get("result", {})

                    return f"""
Vamos interpretar o resultado:

Valor final: {result.get('final_amount', 'N/A')}
Juros obtidos: {result.get('interest_gained', 'N/A')}

Isso mostra como o dinheiro cresce ao longo do tempo com juros.

Resumo:
Quanto maior o tempo e a taxa, maior o crescimento.
"""

                # 🎯 GENERIC
                return "Aqui está uma explicação simplificada baseada no contexto fornecido."

            return "Explicação gerada (modo mock)."

        except Exception:
            return "Não consegui gerar a explicação, mas o sistema continua funcionando."

    # =========================
    # REAL LLM (OPENAI)
    # =========================
    def _real_generate(self, prompt, context, system_prompt):

        if not self.api_key:
            return self._fallback_response(context)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)

            full_prompt = f"""
{system_prompt or "Você é um assistente financeiro inteligente."}

Pergunta:
{prompt}

Contexto:
{context}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
            )

            return response.choices[0].message.content

        except Exception:
            return self._fallback_response(context)

    # =========================
    # FALLBACK (NUNCA QUEBRA)
    # =========================
    def _fallback_response(self, context):

        try:
            if isinstance(context, dict):

                if "concept" in context:
                    concept = context.get("concept", {})
                    return concept.get("definition", "Não consegui explicar, mas este é o conceito.")

                if "result" in context:
                    return f"Resultado calculado: {context.get('result')}"

            return "Não consegui gerar uma explicação detalhada, mas o sistema está funcional."

        except Exception:
            return "Erro ao gerar resposta, mas o sistema continua ativo."

    # =========================
    # EXPLAIN FROM REASONING
    # =========================
    def explain_from_reasoning(self, query, reasoning_data, user_profile):

        return self.generate(
            prompt=query,
            context=reasoning_data,
            system_prompt=f"""
Explique de forma clara e didática.

Nível do usuário: {user_profile.get('level', 'beginner') if user_profile else 'beginner'}
"""
        )