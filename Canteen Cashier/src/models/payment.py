#Coder : Andy
#Class Payment merepresentasikan proses pembayaran dengan memvalidasi jumlah uang yang dibayarkan 
#agar mencukupi total transaksi serta menghitung uang kembalian secara otomatis.
from dataclasses import dataclass
@dataclass(frozen=True)
class Payment:
    amount_paid: int
    total: int
    def __post_init__(self) -> None:
        if isinstance(self.amount_paid, bool) or not isinstance(self.amount_paid, int):
            raise ValueError("Payment must be a whole-rupiah amount.")
        if self.amount_paid < self.total:
            raise ValueError("Payment is less than the total.")
    @property
    def change(self) -> int:
        return self.amount_paid - self.total