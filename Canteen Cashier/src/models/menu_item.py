# Coder : Andy
# Class MenuItem merepresentasikan data menu makanan atau minuman, seperti ID, nama, kategori, dan harga, 
# serta memastikan data yang dimasukkan valid sebelum digunakan dalam aplikasi.
from dataclasses import dataclass
@dataclass(frozen=True)
class MenuItem:
    id: str
    name: str
    category: str
    price: int
    def __post_init__(self) -> None:
        if not self.id or not self.name or not self.category:
            raise ValueError("Menu ID, name, and category are required.")
        if isinstance(self.price, bool) or not isinstance(self.price, int) or self.price <= 0:
            raise ValueError("Menu price must be a positive whole number.")
    @classmethod
    def from_dict(cls, data: dict) -> "MenuItem":
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            price=int(data["price"]),
        )