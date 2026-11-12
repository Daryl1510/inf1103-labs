class Supplier:
    """Who supplied a product.

    Relationship: ASSOCIATION with Product. A Supplier is not part of a Product and
    a Product is not part of a Supplier - they simply know about each other.
    A Supplier is created independently and lives on even if no products use it.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # Read-only access, same encapsulation style as Product.
    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        """Print the supplier's own information."""
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, object]:
        """Return the supplier data as a dictionary (used when saving to JSON)."""
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }
