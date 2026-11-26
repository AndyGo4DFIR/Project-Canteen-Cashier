# ERIC
from uuid import uuid4

from ..models import Cart, Order, Payment
from ..utils.datetime_helper import current_timestamp
from ..utils.validators import validate_payment
from .pricing_service import PricingService
from .storage_service import StorageService


class OrderService:
    def __init__(
        self,
        storage: StorageService,
        pricing: PricingService,
    ) -> None:
        self.storage = storage
        self.pricing = pricing
        self.orders = storage.load_orders()

    def checkout(self, cart: Cart, amount_paid: int) -> Order:
        if cart.is_empty:
            raise ValueError("The cart is empty.")
        quote = self.pricing.calculate(cart)
        validate_payment(amount_paid, quote.total)
        payment = Payment(amount_paid, quote.total)

        order = Order(
            id=uuid4().hex[:8].upper(),
            created_at=current_timestamp(),
            items=[
                {
                    "id": item.menu_item.id,
                    "name": item.menu_item.name,
                    "price": item.menu_item.price,
                    "quantity": item.quantity,
                    "line_total": item.line_total,
                }
                for item in cart.items
            ],
            subtotal=quote.subtotal,
            combo_discount=quote.combo_discount,
            order_discount=quote.order_discount,
            total=quote.total,
            amount_paid=payment.amount_paid,
            change=payment.change,
        )
        updated_orders = [*self.orders, order]
        self.storage.save_orders(updated_orders)
        self.orders.append(order)
        cart.clear()
        return order
