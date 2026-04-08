class FinanceEngine:

    def __init__(self, transactions):

        self.transactions = transactions

    def total_spending(self):

        return sum(t["amount"] for t in self.transactions)

    def spending_by_category(self):

        result = {}

        for t in self.transactions:

            cat = t["category"]

            if cat not in result:
                result[cat] = 0

            result[cat] += t["amount"]

        return result

    def highest_category(self):

        categories = self.spending_by_category()

        if not categories:
            return None

        return max(categories, key=categories.get)
        
    def summary(self):

        total = self.total_spending()
        by_cat = self.spending_by_category()

        return {
            "total": total,
            "categories": by_cat
        }