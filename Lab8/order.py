from order_line import OrderLine
from product import Product


class Order:
    """A customer order, made up of OrderLine objects.

    Relationship: COMPOSITION with OrderLine. The Order CREATES and manages its own
    lines - add_order_line() takes a Product and a quantity (NOT a ready-made
    OrderLine) and builds the OrderLine internally. If the order is cancelled, its
    lines go with it. The Products referred to by the lines are NOT affected.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        """A copy of the list - outside code cannot add or swap lines directly."""
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine inside this order for the given product."""
        order_line = OrderLine(product, quantity)      # the Order creates its own part
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product ID (managed by the Order, not from outside).
        Returns True if a line was removed, False if none matched."""
        for order_line in self.__order_lines:
            if order_line.product.product_id.upper() == product_id.upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    def cancel(self) -> None:
        """Cancel the order: all of its lines are removed with it."""
        self.__order_lines.clear()

    def calculate_total(self) -> float:
        """Ask each OrderLine for its subtotal and add them up."""
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        if not self.__order_lines:
            print("    (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"    Total: ${self.calculate_total():.2f}")
