class StakeHistoryReport:

    def __init__(self, transactions):
        self.transactions = transactions

        self.total_transactions = len(transactions)

        self.total_credit = sum(
            t["amount"] for t in transactions if t["amount"] > 0
        )

        self.total_debit = sum(
            abs(t["amount"]) for t in transactions if t["amount"] < 0
        )

        self.net_profit = self.total_credit - self.total_debit

        # breakdown
        self.type_breakdown = {}
        for t in transactions:
            t_type = t["transaction_type"]
            self.type_breakdown[t_type] = self.type_breakdown.get(t_type, 0) + 1

    def to_dict(self):
        return {
            "total_transactions": self.total_transactions,
            "total_credit": self.total_credit,
            "total_debit": self.total_debit,
            "net_profit": self.net_profit,
            "type_breakdown": self.type_breakdown,
            "transactions": self.transactions
        }