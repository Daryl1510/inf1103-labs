from product import Product



class DigitalProduct(Product):
    """A product delivered electronically. It does not need shipping,
    so it does NOT implement CanBeShipped."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)   # reuse Product's constructor
        self.__download_size = download_size                # in megabytes

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()                       # parent prints the common info
        print(f"    Type: Digital | Download size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "Digital product: delivered digitally via download link."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
