from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from src.utils.validators import validate_money, validate_payment
class PaymentMethod(Enum):
  CASH = "cash"
  CARD = "card"
  EWALLET = "ewallet"
class PaymentStatus(Enum):
  PENDING ="pending"
  PAID ="paid"
@dataclass
class Payment:
  method: PaymentMethod
  amount_due: Decimal
  amount_paid: Decimal = field(default=Decimal("0.00"))
  status: PaymentStatus=PaymentStatus.PENDING
  def __post_init__(self):
    self.amout_due=validate_money(self.amount_due, "amount_due")
  def pay(self, amount_paid)->None:
    self.amount_paid=validate_payment(self.method, amount_paid, self.amount_due)
    self.status=PaymentStatus.PAID
  @property
  def change(self)->Decimal:
    if self.status is not PaymentStatus.PAID:
      return Decimal("0.00")
    return self.amount_paid - self.amount_due