# Coder : Andy
# Class CartItem merepresentasikan item menu beserta jumlah dan total harganya, 
# sedangkan class Cart berfungsi mengelola kumpulan item pesanan dalam keranjang belanja.
from dataclasses import dataclass
from .menu_item import MenuItem
@dataclass
class CartItem:
    menu_item: MenuItem
    quantity: int = 1
    @property
    def line_total(self) -> int:
        return self.menu_item.price * self.quantity
class Cart:
    def __init__(self) -> None:
        self._items: dict[str, CartItem] = {}
    @property
    def items(self) -> list[CartItem]:
        return list(self._items.values())
    @property
    def is_empty(self) -> bool:
        return not self._items
    @property
    def subtotal(self) -> int:
        return sum(item.line_total for item in self._items.values())
    def quantity_of(self, menu_item_id: str) -> int:
        item = self._items.get(menu_item_id)
        return item.quantity if item else 0
    def add(self, menu_item: MenuItem) -> None:
        item = self._items.get(menu_item.id)
        if item:
            item.quantity += 1
        else:
            self._items[menu_item.id] = CartItem(menu_item)
    def remove_one(self, menu_item_id: str) -> None:
        if menu_item_id not in self._items:
            raise KeyError("This item is not in the cart.")
        item = self._items[menu_item_id]
        item.quantity -= 1
        if item.quantity <= 0:
            del self._items[menu_item_id]
    def clear(self) -> None:
        self._items.clear()