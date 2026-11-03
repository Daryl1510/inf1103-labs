from abc import ABC, abstractmethod



class CanBeShipped(ABC):
    """Interface-style contract: anything that can be shipped must be able to
    calculate its own shipping cost.

    Deliberately contains no attributes and no implementation details.
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this item."""
        pass
