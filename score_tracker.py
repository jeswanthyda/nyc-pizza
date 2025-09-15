class ScoreTracker:
    """Tracks game score, earnings, spending, and subway usage."""

    def __init__(self):
        self.score = 0  # Net income (earned - spent)
        self.earned = 0  # Money earned from pizza deliveries
        self.spent = 0  # Money spent on subway usage
        self.subway_usage_count = 0  # Track subway usage for cost calculation

    def update_score(self):
        """Update the net income score."""
        self.score = self.earned - self.spent

    def earn_money(self, amount: int):
        """Add money to earned amount and update score."""
        self.earned += amount
        self.update_score()

    def spend_money(self, amount: int):
        """Add money to spent amount and update score."""
        self.spent += amount
        self.update_score()

    def use_subway(self):
        """Record subway usage and spend $1."""
        self.subway_usage_count += 1
        self.spend_money(1)
