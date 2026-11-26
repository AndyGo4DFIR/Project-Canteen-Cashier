#Coder : Andy
#Class PriceQuote menyimpan hasil perhitungan harga dan diskon, 
#sedangkan class PricingService mengelola proses perhitungan subtotal, diskon combo, diskon transaksi, dan total pembayaran pesanan.
from dataclasses import dataclass
from ..models import Cart
@dataclass(frozen=True)
class PriceQuote:
    subtotal: int
    combo_discount: int
    order_discount: int
    @property
    def total_discount(self) -> int:
        return self.combo_discount + self.order_discount
    @property
    def total(self) -> int:
        return self.subtotal - self.total_discount
class PricingService:
    COMBO_RATE = 0.10
    ORDER_DISCOUNT_THRESHOLD = 150_000
    ORDER_DISCOUNT_RATE = 0.05
    MAIN_CATEGORIES = {"Main", "Rice Bowl"}
    DRINK_CATEGORIES = {"Drink"}
    def calculate(self, cart: Cart) -> PriceQuote:
        subtotal = cart.subtotal
        main_count = sum(
            item.quantity
            for item in cart.items
            if item.menu_item.category in self.MAIN_CATEGORIES
        )
        drink_prices = [
            item.menu_item.price
            for item in cart.items
            if item.menu_item.category in self.DRINK_CATEGORIES
            for _ in range(item.quantity)
        ]
        combo_count = min(main_count, len(drink_prices))
        combo_discount = sum(
            round(price * self.COMBO_RATE)
            for price in sorted(drink_prices)[:combo_count]
        )
        discounted_subtotal = subtotal - combo_discount
        order_discount = (
            round(discounted_subtotal * self.ORDER_DISCOUNT_RATE)
            if subtotal >= self.ORDER_DISCOUNT_THRESHOLD
            else 0
        )
        return PriceQuote(subtotal, combo_discount, order_discount)