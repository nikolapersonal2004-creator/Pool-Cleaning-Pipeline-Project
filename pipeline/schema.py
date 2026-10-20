"""The structure of a valid pool-cleaning transaction."""


class TransactionRecord:
    """Keep the information for one service job together."""

    def __init__(self, branch_id, transaction_date, customer_tier,
                 item_count, revenue, cost, province, active):
        # These values have already been checked by validator.py.
        self.branch_id = branch_id
        self.transaction_date = transaction_date
        self.customer_tier = customer_tier
        self.item_count = item_count
        self.revenue = revenue
        self.cost = cost
        self.province = province
        self.active = active
