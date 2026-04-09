# core/rag_engine.py

from typing import List, Dict, Any


class RAGEngine:
    def __init__(self, graph_engine):
        self.graph_engine = graph_engine

    # =========================
    # MAIN RETRIEVE (MANTIDO + EVOLUÍDO)
    # =========================
    def retrieve(self, query: str) -> List[Dict]:
        """
        Retorna contexto estruturado do grafo
        """

        # 🔹 usa search do graph (novo)
        raw_relations = self.graph_engine.search(query)

        # 🔹 normaliza saída
        return self._structure_context(raw_relations)

    # =========================
    # NOVO: ESTRUTURAR CONTEXTO
    # =========================
    def _structure_context(self, relations: List[Dict]) -> List[Dict]:
        structured = []

        for rel in relations:
            structured.append({
                "source": rel.get("source"),
                "target": rel.get("target"),
                "type": rel.get("type", "correlational"),
                "effect": rel.get("effect", ""),
                "weight": rel.get("weight", 0.5),
            })

        return structured

    # =========================
    # NOVO: CONTEXTO EXPANDIDO
    # =========================
    def retrieve_expanded(self, query: str, depth: int = 1) -> List[Dict]:
        """
        Usa expansão do grafo (multi-hop reasoning base)
        """

        concept = self.graph_engine.find_concept(query)

        if not concept:
            return self.retrieve(query)

        concept_id = concept.get("id")

        expanded = self.graph_engine.expand_graph(
            concept_id=concept_id,
            depth=depth
        )

        return self._structure_context(expanded)

    # =========================
    # NOVO: CONTEXTO PARA LLM
    # =========================
    def to_llm_context(self, relations: List[Dict]) -> str:
        """
        Converte estrutura para leitura do LLM
        """

        lines = []

        for r in relations:
            lines.append(
                f"{r['source']} → {r['target']} | {r['type']} | effect: {r['effect']} | weight: {r['weight']}"
            )

        return "\n".join(lines)