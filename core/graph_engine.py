import json
import networkx as nx


class FinancialGraph:

    def __init__(self, concepts_file, relations_file):

        self.graph = nx.DiGraph()

        self.load_concepts(concepts_file)
        self.load_relations(relations_file)

    def load_concepts(self, file):

        with open(file, encoding="utf-8") as f:
            concepts = json.load(f)

        for c in concepts:

            self.graph.add_node(
                c["id"],
                name=c.get("name", ""),
                module=c.get("module", ""),
                definition=c.get("definition", ""),
                difficulty=c.get("difficulty", "iniciante")
            )

    def load_relations(self, file):

        with open(file, encoding="utf-8") as f:
            relations = json.load(f)

        for r in relations:

            self.graph.add_edge(
                r["source"],
                r["target"],
                relation=r["relation"],
                weight=r.get("weight", 0.5)
            )

    def neighbors(self, concept):

        return list(self.graph.neighbors(concept))

    def get_relation(self, source, target):

        return self.graph[source][target]

    def get_definition(self, concept):

        return self.graph.nodes[concept].get("definition", "")

    def get_module(self, concept):

        return self.graph.nodes[concept].get("module", "")