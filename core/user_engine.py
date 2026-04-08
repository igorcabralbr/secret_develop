class UserProfile:

    def __init__(self, age_group, level):

        self.age_group = age_group
        self.level = level

    def adapt_text(self, text):

        if self.level == "iniciante":
            text = f"Vamos simplificar: {text}"

        elif self.level == "avancado":
            text = f"Análise técnica: {text}"

        if self.age_group == "teen":
            text = f"Imagina assim: {text}"

        elif self.age_group == "elderly":
            text = f"Vou explicar com calma: {text}"

        return text

    def communication_style(self):

        if self.age_group == "teen":
            return "informal"

        if self.age_group == "elderly":
            return "didatic"

        return "normal"