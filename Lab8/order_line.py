from product import Product


class OrderLine:
    """One product and the quantity requested of it, inside ONE order.

    Relationships:
      - COMPOSITION (part side) with Order: an OrderLine only makes sense inside the
        Order that created it. It is not meant to be created elsewhere, shared, or
        moved to another Order. (Python can't enforce this - the design intends it.)
      - ASSOCIATION with Product: it refers to a Product but does NOT own it.
        The Product lives on independently (e.g. it may also sit in an Inventory).
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"    {self.__product.name} (ID: {self.__product.product_id}) | "
              f"Qty: {self.__quantity} | Unit: ${self.__product.price:.2f} | "
              f"Subtotal: ${self.calculate_subtotal():.2f}")
