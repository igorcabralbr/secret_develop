class MentorEngine:

    def __init__(self, graph):

        self.graph = graph

    def analyze(self, income, expenses):

        total_expenses = sum(e["amount"] for e in expenses)

        savings = income - total_expenses

        savings_rate = savings / income if income > 0 else 0

        categories = {}
        for e in expenses:
            categories.setdefault(e["category"], 0)
            categories[e["category"]] += e["amount"]

        insights = []

        # 🧠 regras simples mas poderosas

        if savings_rate < 0.1:
            insights.append("Você está economizando pouco.")

        if savings_rate > 0.3:
            insights.append("Ótima taxa de poupança.")

        if "lazer" in categories and categories["lazer"] > income * 0.2:
            insights.append("Gastos com lazer estão altos.")

        if "moradia" in categories and categories["moradia"] > income * 0.4:
            insights.append("Custo de moradia elevado.")

        # recomendação base
        recommendation = "Tente manter uma taxa de poupança entre 20% e 30%."

        return {
            "income": income,
            "expenses": total_expenses,
            "savings": savings,
            "savings_rate": round(savings_rate, 2),
            "insights": insights,
            "recommendation": recommendation,
            "categories": categories
        }