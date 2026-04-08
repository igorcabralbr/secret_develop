class RAGEngine:

    def __init__(self, graph):

        self.graph = graph

    def explain_concept(self, concept_id):

        definition = self.graph.get_definition(concept_id)

        module = self.graph.get_module(concept_id)

        return {
            "concept": concept_id,
            "module": module,
            "definition": definition
        }

    def related_concepts(self, concept_id):

        neighbors = self.graph.neighbors(concept_id)

        return neighbors[:10]