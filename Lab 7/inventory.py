class Inventory:
    """Manages a collection of Product objects.

    Responsibility (SRP): store, add, search and display products.
    It does NOT read user input or handle files.
    """

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Returns False if the ID already exists, otherwise True."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def display_all(self):
        """Print every product, or a message if the inventory is empty."""
        print("\nCurrent Inventory")
        if self.is_empty():
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()

    def is_empty(self):
        return len(self.__products) == 0

    def to_list(self):
        """Return all products as a list of dictionaries (used when saving to JSON)."""
        return [product.to_dict() for product in self.__products]


