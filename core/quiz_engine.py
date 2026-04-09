# core/quiz_engine.py

import random
from typing import Dict, List, Any


class QuizEngine:
    def __init__(self, graph_engine, llm_engine=None):
        self.graph_engine = graph_engine
        self.llm_engine = llm_engine  # 🔥 opcional (não obrigatório)

    # =========================
    # MAIN GENERATE (EVOLUÍDO)
    # =========================
    def generate(self, query: str, user_context: Dict = None) -> Dict:

        concept = self._extract_concept(query)

        if not concept:
            concept = self._fallback_concept()

        difficulty = self._get_difficulty(user_context)

        relations = self.graph_engine.get_related(concept.get("id"))

        quiz = self._build_quiz(concept, relations, difficulty)

        # 🤖 LLM opcional (apenas refino textual)
        if self.llm_engine:
            quiz = self._beautify_with_llm(quiz, user_context)

        return quiz

    # =========================
    # CONCEPT EXTRACTION
    # =========================
    def _extract_concept(self, query: str) -> Dict:
        return self.graph_engine.find_concept(query)

    # =========================
    # FALLBACK
    # =========================
    def _fallback_concept(self) -> Dict:
        if self.graph_engine.concepts:
            return random.choice(self.graph_engine.concepts)
        return {}

    # =========================
    # DIFFICULTY ENGINE
    # =========================
    def _get_difficulty(self, user_context: Dict) -> str:

        if not user_context:
            return "beginner"

        level = user_context.get("level", "beginner")

        return level

    # =========================
    # BUILD QUIZ (CORE LOGIC)
    # =========================
    def _build_quiz(self, concept: Dict, relations: List[Dict], difficulty: str) -> Dict:

        question = self._generate_question(concept, difficulty)

        options = self._generate_options(concept, relations)

        correct = options[0]  # simplificado (pode evoluir depois)

        random.shuffle(options)

        return {
            "type": "quiz",
            "concept": concept.get("name"),
            "difficulty": difficulty,
            "question": question,
            "options": options,
            "answer": correct
        }

    # =========================
    # QUESTION GENERATOR
    # =========================
    def _generate_question(self, concept: Dict, difficulty: str) -> str:

        name = concept.get("name", "conceito")

        if difficulty == "beginner":
            return f"O que é {name}?"

        if difficulty == "intermediate":
            return f"Como {name} influencia a economia?"

        return f"Analise o impacto sistêmico de {name} no cenário econômico."

    # =========================
    # OPTIONS GENERATOR
    # =========================
    def _generate_options(self, concept: Dict, relations: List[Dict]) -> List[str]:

        correct = concept.get("definition", f"Definição de {concept.get('name')}")

        distractors = [
            "Um conceito sem relação econômica direta",
            "Um tipo de imposto governamental",
            "Um indicador financeiro irrelevante"
        ]

        options = [correct] + distractors[:3]

        return options

    # =========================
    # LLM ENHANCEMENT (NOVO)
    # =========================
    def _beautify_with_llm(self, quiz: Dict, user_context: Dict) -> Dict:

        try:
            refined = self.llm_engine.generate(
                prompt=f"""
Melhore este quiz sem alterar respostas corretas:

{quiz}

Adapte linguagem para nível: {user_context.get('level', 'beginner') if user_context else 'beginner'}
""",
                system_prompt="""
Você é um criador de quizzes educacionais.
Mantenha as respostas corretas inalteradas.
Melhore apenas linguagem e clareza.
"""
            )

            return {
                **quiz,
                "llm_refinement": refined
            }

        except Exception:
            return quiz