class AccessibilityEngine:

    def __init__(self, mode="normal"):

        self.mode = mode

    def format_text(self, text):

        if self.mode == "high_contrast":

            return text.upper()

        if self.mode == "simple":

            sentences = text.split(".")

            short = sentences[:2]

            return ".".join(short)

        if self.mode == "neurodivergent":

            return text.replace(",", "\n")

        return text

    def libras_placeholder(self):

        return "Integração com API de avatar em Libras aqui."