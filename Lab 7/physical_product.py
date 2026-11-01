from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.

    Single inheritance from Product, plus it signs the CanBeShipped interface.
    """

    BASE_SHIPPING_FEE = 5.00     # flat fee for any shipment ($)
    RATE_PER_KG = 2.00           # additional charge per kilogram ($)

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)   # reuse Product's constructor
        self.__weight = weight                              # in kilograms

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()                       # parent prints the common info
        print(f"    Type: Physical | Weight: {self.__weight} kg")   # child adds its own

    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."

    def calculate_shipping_cost(self):
        """Simple rule: flat base fee plus a charge per kilogram."""
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
