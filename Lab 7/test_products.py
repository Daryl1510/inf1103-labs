"""Quick checks for Lab 7 (sections 1-4 and 7). Run with: python test_products.py"""
from product import Product
from can_be_shipped import CanBeShipped
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def heading(text):
    print(f"\n=== {text} ===")


# 1. Physical products store and display their weight
heading("PhysicalProduct display_information()")
guitar = PhysicalProduct("P100", "Guitar", 450.00, 5, 3.5)
guitar.display_information()

# 2. Digital products store and display their download size
heading("DigitalProduct display_information()")
os_disk = DigitalProduct("D100", "Operating System", 129.99, 999, 4200)
os_disk.display_information()

# 3. Both subclasses implement get_fulfilment_info()
heading("get_fulfilment_info()")
print(guitar.get_fulfilment_info())
print(os_disk.get_fulfilment_info())

# 4. The abstract Product class cannot be instantiated directly
heading("Instantiating abstract Product")
try:
    Product("X001", "Generic", 1.00, 1)
    print("FAIL: Product was created directly")
except TypeError as error:
    print(f"OK - TypeError raised: {error}")

# 5. The interface cannot be instantiated either
heading("Instantiating CanBeShipped interface")
try:
    CanBeShipped()
    print("FAIL: CanBeShipped was created directly")
except TypeError as error:
    print(f"OK - TypeError raised: {error}")

# 6. Physical products calculate shipping costs (different weights)
heading("calculate_shipping_cost()")
for item in (PhysicalProduct("P101", "Mouse", 25.50, 40, 0.1),
             PhysicalProduct("P102", "Laptop", 1200.00, 15, 2.2),
             PhysicalProduct("P103", "Monitor", 299.99, 10, 6.0)):
    print(f"{item.name} ({item.weight} kg): shipping ${item.calculate_shipping_cost():.2f}")

# 7. Digital products are not required to implement shipping
heading("Digital products and shipping")
print("DigitalProduct is a CanBeShipped:", isinstance(os_disk, CanBeShipped))
print("DigitalProduct has calculate_shipping_cost:", hasattr(os_disk, "calculate_shipping_cost"))
print("PhysicalProduct is a CanBeShipped:", isinstance(guitar, CanBeShipped))

# 8. Stock updates still work through the inherited method
heading("update_stock() inherited from Product")
print("Update to 10 accepted:", guitar.update_stock(10), "-> stock is now", guitar.stock)
print("Update to -5 accepted:", guitar.update_stock(-5), "-> stock is still", guitar.stock)

# 9. to_dict() carries the type and extra attributes (used for JSON saving)
heading("to_dict()")
print(guitar.to_dict())
print(os_disk.to_dict())
