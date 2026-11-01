from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for every product in the system.

    Responsibility (SRP): store the information common to all products and
    control how it changes. Cannot be instantiated directly - every product
    must be a specialised type (physical or digital).
    """

    def __init__(self, product_id, name, price, stock):
        # Double underscore = "private" by convention (Python name-mangles these).
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Read-only access: outside code can look, but must use methods to change.
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Set the stock to a new quantity. Returns True if accepted, False if not."""
        if not isinstance(quantity, int) or quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        """Print the information common to all products."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Return the common product data as a dictionary (used when saving to JSON)."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        """Every product type must say how it is fulfilled (shipped, downloaded, ...)."""
        pass
