from dataclasses import dataclass
from src.utils.validators import validate_qty, validate_stock
class InsufficientStockError(Exception):
  pass
@dataclass
class InventoryItem:
  item_id: str
  stock: int
  def __post_init__(self):
    self.stock=validate_stock(self.stock)
  def has_stock(self, qty: int)->bool:
    return self.stock >= validate_qty(qty)
  def reduce(self, qty: int)->None:
    if not self.has_stock(qty):
      raise InsufficientStockError(f"{self.item_id}: need {qty}, only{self.stock} left")
    self.stock -= qty
  def restore(self, qty:int)->None:
    self.stock += validate_qty(qty)