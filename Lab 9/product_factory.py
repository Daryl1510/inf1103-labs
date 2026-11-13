from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """Centralises product creation (Factory pattern).

    The rest of the program asks the factory for a Product and only needs to know
    about the Product type - not about PhysicalProduct or DigitalProduct.
    Trade-off: when a new product type is added, THIS class changes (it still
    breaks Open/Closed), but it is the only place that has to. For an application
    this small, that is an acceptable cost.

    Relationship: DEPENDENCY on Product. The factory creates products but does not
    store them.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        """Build and return the right kind of Product.

        weight is only used for "physical" and download_size only for "digital".
        Both default to 0.0, which means 'not provided' (e.g. rows from products.csv
        have no such column).
        Raises ValueError for an unknown product type, or for invalid values
        (the Product classes validate price and stock themselves).
        """
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
