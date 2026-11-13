from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered electronically. It does not need shipping,
    so it does NOT implement CanBeShipped.

    LSP note: it does NOT override update_stock(). A digital product still has a
    stock figure (e.g. licence keys / copies available), so Product's version of
    update_stock() is exactly right and is inherited unchanged.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 download_size: float, supplier: Supplier) -> None:
        # reuse Product's constructor (it stores the supplier reference too)
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size         # in megabytes

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()                       # parent prints the common info
        print(f"    Type: Digital | Download size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered digitally via download link."

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
