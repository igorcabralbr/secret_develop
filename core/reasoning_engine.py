class ReasoningEngine:

    def __init__(self, graph):

        self.graph = graph.graph

    def find_paths(self, start, depth=4):

        paths = []

        def dfs(node, path, current_weight, d):

            if d == 0:
                return

            for neighbor in self.graph.neighbors(node):

                edge = self.graph[node][neighbor]

                relation = edge["relation"]
                weight = edge.get("weight", 0.5)

                new_path = path + [(node, relation, neighbor)]

                score = current_weight * weight

                paths.append({
                    "path": new_path,
                    "score": score
                })

                dfs(neighbor, new_path, score, d - 1)

        dfs(start, [], 1.0, depth)

        paths.sort(key=lambda x: x["score"], reverse=True)

        return paths[:10]