from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product in the system.

    Responsibility (SRP): store the information common to all products and
    control how it changes. Cannot be instantiated directly - every product
    must be a specialised type (physical or digital).

    Relationship: ASSOCIATION with Supplier. The Supplier is created independently
    and handed in; Product only keeps a reference to it (it does not own it).

    Validation (Lab 9): the rules for price and stock live HERE, in the class that
    owns them. PhysicalProduct and DigitalProduct inherit them through super().__init__
    and update_stock(), so every Product type obeys the same rules (LSP).
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if not price > 0:                 # written this way so NaN is rejected too
            raise ValueError("Price must be greater than zero.")
        Product.__check_stock(stock)
        # Double underscore = "private" by convention (Python name-mangles these).
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier      # reference only - NOT owned

    # Read-only access: outside code can look, but must use methods to change.
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    @staticmethod
    def __check_stock(quantity: int) -> None:
        """The single stock rule, shared by the constructor and update_stock()."""
        if not isinstance(quantity, int):
            raise ValueError("Stock quantity must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

    def update_stock(self, quantity: int) -> None:
        """Set the stock to a new quantity.

        This is the contract EVERY subclass must keep (Liskov Substitution):
        a whole number >= 0 is accepted; anything else raises ValueError and
        leaves the stock unchanged.
        """
        Product.__check_stock(quantity)
        self.__stock = quantity

    def display_information(self) -> None:
        """Print the information common to all products."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def display_supplier(self) -> None:
        """Show the supplier's details, by asking the Supplier to display itself."""
        self.__supplier.display_information()

    def to_dict(self) -> dict[str, object]:
        """Return the common product data as a dictionary (used when saving to JSON)."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Every product type must say how it is fulfilled (shipped, downloaded, ...)."""
        pass
