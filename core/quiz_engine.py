import random
import json


class QuizEngine:

    def __init__(self, relations_file, concepts_file):

        with open(relations_file, encoding="utf-8") as f:
            self.relations = json.load(f)

        with open(concepts_file, encoding="utf-8") as f:
            concepts = json.load(f)

        self.concept_ids = [c["id"] for c in concepts]

    def generate_quiz(self):

        r = random.choice(self.relations)

        question = f"O que pode acontecer se {r['source']} aumentar?"

        correct = r["target"]

        options = [correct]

        while len(options) < 4:

            opt = random.choice(self.concept_ids)

            if opt not in options:
                options.append(opt)

        random.shuffle(options)

        return {
            "question": question,
            "options": options,
            "correct": correct
        }