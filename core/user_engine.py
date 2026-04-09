# core/user_engine.py

from typing import Dict, Optional
import json
import os


class UserEngine:
    def __init__(self, storage_path: str = "data/users.json"):
        self.storage_path = storage_path
        self.users = self._load_users()

    # =========================
    # LOAD / SAVE
    # =========================
    def _load_users(self) -> Dict:
        if not os.path.exists(self.storage_path):
            return {}

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_users(self):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=2)

    # =========================
    # GET USER (MANTIDO + MELHORADO)
    # =========================
    def get_user(self, user_id: str) -> Dict:
        """
        Retorna usuário com fallback inteligente
        """

        if user_id not in self.users:
            # 🔹 cria usuário padrão automaticamente
            self.users[user_id] = self._create_default_user(user_id)
            self._save_users()

        return self.users[user_id]

    # =========================
    # CREATE DEFAULT USER
    # =========================
    def _create_default_user(self, user_id: str) -> Dict:
        return {
            "user_id": user_id,
            "level": "beginner",
            "age_group": "adult",

            # 🔥 NOVO: perfil cognitivo
            "learning_style": "visual",
            "financial_experience": "low",

            # 🔥 NOVO: histórico de interação
            "interaction_count": 0,

            # 🔥 NOVO: preferências
            "preferences": {
                "explanation_depth": "medium",
                "use_examples": True,
                "use_analogies": True
            }
        }

    # =========================
    # UPDATE USER (MELHORADO)
    # =========================
    def update_user(self, user_id: str, updates: Dict):
        user = self.get_user(user_id)

        for key, value in updates.items():
            if isinstance(value, dict) and key in user:
                user[key].update(value)
            else:
                user[key] = value

        self.users[user_id] = user
        self._save_users()

    # =========================
    # NOVO: INCREMENTA INTERAÇÃO
    # =========================
    def increment_interaction(self, user_id: str):
        user = self.get_user(user_id)
        user["interaction_count"] += 1

        # 🔥 auto evolução simples de nível
        if user["interaction_count"] > 10:
            user["level"] = "intermediate"
        if user["interaction_count"] > 30:
            user["level"] = "advanced"

        self._save_users()

    # =========================
    # NOVO: PERFIL PARA LLM
    # =========================
    def get_llm_profile(self, user_id: str) -> Dict:
        """
        Formata usuário para o LLM entender melhor
        """

        user = self.get_user(user_id)

        return {
            "level": user.get("level"),
            "age_group": user.get("age_group"),
            "learning_style": user.get("learning_style"),
            "preferences": user.get("preferences")
        }

    # =========================
    # NOVO: CONTEXTO PARA ORQUESTRADOR
    # =========================
    def get_context(self, user_id: str) -> Dict:
        """
        Contexto completo para o BrainOrchestrator
        """

        user = self.get_user(user_id)

        return {
            "profile": user,
            "level": user.get("level"),
            "is_beginner": user.get("level") == "beginner",
            "is_advanced": user.get("level") == "advanced"
        }