class UserProfile:

    def __init__(self, age_group, level):

        self.age_group = age_group
        self.level = level

    def adapt_text(self, text):

        if self.level == "iniciante":

            return f"Explicação simples: {text}"

        if self.level == "avancado":

            return f"Explicação técnica: {text}"

        return text

    def communication_style(self):

        if self.age_group == "teen":
            return "informal"

        if self.age_group == "elderly":
            return "didatic"

        return "normal"