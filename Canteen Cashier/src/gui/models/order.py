# ERIC
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    id: str
    created_at: str
    items: list[dict]
    subtotal: int
    combo_discount: int
    order_discount: int
    total: int
    amount_paid: int
    change: int

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "items": self.items,
            "subtotal": self.subtotal,
            "combo_discount": self.combo_discount,
            "order_discount": self.order_discount,
            "total": self.total,
            "amount_paid": self.amount_paid,
            "change": self.change,
        }
