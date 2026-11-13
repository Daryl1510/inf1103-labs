from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """A fourth strategy: 5% off for students (Section 2.4).

    Notice what did NOT change to add this: Order, OrderLine and the other
    strategies are untouched. The new behaviour lives in its own new class.
    """

    RATE: float = 0.05          # 5%

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)
