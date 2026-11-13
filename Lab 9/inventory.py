from product import Product


class Inventory:
    """Manages a collection of Product objects.

    Responsibility (SRP): store, add, remove, find and display products.
    It does NOT read user input or handle files.

    Relationship: AGGREGATION with Product. The Inventory holds references to
    products but does not create them or control their lifecycle. A product can
    exist before it is added, and can be removed or moved to another Inventory
    without being destroyed.

    LSP: the collection is typed with the BASE class Product, and no method here
    checks whether an item is a PhysicalProduct or a DigitalProduct.
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        """A copy of the list, so outside code cannot change the collection directly."""
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists, otherwise True."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the matching Product from this inventory and return it.

        Only the reference is removed - the Product object itself is NOT destroyed,
        so the caller can keep using it or add it to another Inventory.
        Returns None if no product matches.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def display_all(self) -> None:
        """Print every product, or a message if the inventory is empty."""
        print("\nCurrent Inventory")
        if self.is_empty():
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()      # each product picks its own version

    def is_empty(self) -> bool:
        return len(self.__products) == 0

    def to_list(self) -> list[dict[str, object]]:
        """Return all products as a list of dictionaries (used when saving to JSON)."""
        return [product.to_dict() for product in self.__products]
