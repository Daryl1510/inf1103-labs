from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """The shared 'shape' of every discount (Strategy pattern).

    Order only ever calls apply(), so it never needs to know HOW a discount works.
    A new kind of discount = a new subclass, with no change to Order (Open/Closed).
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Take an order total and return the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged. Used when an order has no discount."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        # The class that owns the rule protects it (Section 4).
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total
