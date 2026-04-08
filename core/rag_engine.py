class RAGEngine:

    def __init__(self, graph):

        self.graph = graph

    def explain_concept(self, concept_text):

        concept_text = concept_text.lower()

        for node in self.graph.graph.nodes:

            if concept_text in node:
                return {
                    "concept": node,
                    "definition": self.graph.get_definition(node)
                }

        return {"definition": "Conceito não encontrado"}

    def related_concepts(self, concept_id):

        neighbors = self.graph.neighbors(concept_id)

        return neighbors[:10]