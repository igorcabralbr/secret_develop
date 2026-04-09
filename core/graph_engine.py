# core/graph_engine.py

import json
from typing import List, Dict, Any


class GraphEngine:
    def __init__(self, concepts_path: str, relations_path: str):
        self.concepts_path = concepts_path
        self.relations_path = relations_path

        self.concepts = self._load_json(concepts_path)
        self.relations = self._load_json(relations_path)

        # 🔹 NOVO: índices para busca rápida
        self._build_indexes()

    # =========================
    # LOAD
    # =========================
    def _load_json(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    # =========================
    # INDEXAÇÃO (NOVO)
    # =========================
    def _build_indexes(self):
        self.concept_by_id = {}
        self.concept_by_name = {}

        for c in self.concepts:
            cid = c.get("id")
            name = c.get("name", "").lower()

            if cid:
                self.concept_by_id[cid] = c

            if name:
                self.concept_by_name[name] = c

    # =========================
    # FIND CONCEPT (NOVO)
    # =========================
    def find_concept(self, query: str) -> Dict:
        query_lower = query.lower()

        # match direto por nome
        for name, concept in self.concept_by_name.items():
            if name in query_lower:
                return concept

        # fallback: busca parcial
        for concept in self.concepts:
            if concept.get("name", "").lower() in query_lower:
                return concept

        return {}

    # =========================
    # GET RELATED (PADRÃO ORCHESTRATOR)
    # =========================
    def get_related(self, concept_id: str) -> List[Dict]:
        related = []

        for rel in self.relations:
            if rel.get("source") == concept_id:
                related.append(rel)

        return related

    # =========================
    # SEARCH (NOVO - USADO PELO RAG)
    # =========================
    def search(self, query: str) -> List[Dict]:
        """
        Retorna relações relevantes com base no texto
        """

        query_lower = query.lower()
        results = []

        for rel in self.relations:
            source = rel.get("source", "")
            target = rel.get("target", "")

            if source in query_lower or target in query_lower:
                results.append(rel)

        return results

    # =========================
    # GET CONCEPT FULL (NOVO)
    # =========================
    def get_concept_full(self, concept_id: str) -> Dict:
        concept = self.concept_by_id.get(concept_id, {})
        relations = self.get_related(concept_id)

        return {
            "concept": concept,
            "relations": relations
        }

    # =========================
    # EXPAND GRAPH (NOVO)
    # =========================
    def expand_graph(self, concept_id: str, depth: int = 1) -> List[Dict]:
        """
        Expande relações em múltiplos níveis
        """

        visited = set()
        results = []

        def dfs(cid, current_depth):
            if current_depth > depth or cid in visited:
                return

            visited.add(cid)

            relations = self.get_related(cid)

            for rel in relations:
                results.append(rel)
                dfs(rel.get("target"), current_depth + 1)

        dfs(concept_id, 0)
        return results

    # =========================
    # NORMALIZAÇÃO (NOVO)
    # =========================
    def normalize_relation(self, rel: Dict) -> Dict:
        return {
            "source": rel.get("source"),
            "target": rel.get("target"),
            "type": rel.get("type", "correlational"),
            "effect": rel.get("effect", ""),
            "weight": rel.get("weight", 0.5),
        }