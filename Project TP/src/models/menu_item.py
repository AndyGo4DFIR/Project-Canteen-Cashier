from dataclasses import dataclass
from decimal import Decimal
from src.utils.validators import validate_money
@dataclass(frozen=True)
class MenuItem:
  item_id: str
  name: str
  price: Decimal
  category: str = "general"
  def __post_init__(self):
    if not self.item_id.strip():
      raise ValueError("item_id is required")
    if not self.name.strip():
      raise ValueError("name is required")
    object.__setattr__(self, "price", validate_money(self.price, "price"))