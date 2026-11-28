#TIFFANNY
from ..models import Order
from ..utils.datetime_helper import display_timestamp
from ..utils.money import format_rupiah


class ReceiptService:
    @staticmethod
    def render(order: Order, store_name: str) -> str:
        lines = [
            store_name,
            "Payment Receipt",
            f"Order: {order.id}",
            display_timestamp(order.created_at),
            "-" * 34,
        ]
        for item in order.items:
            lines.append(item["name"])
            lines.append(
                f"  {item['quantity']} x {format_rupiah(item['price'])}"
                f" = {format_rupiah(item['line_total'])}"
            )
        lines.extend(
            [
                "-" * 34,
                f"Subtotal: {format_rupiah(order.subtotal)}",
                f"Combo discount: {format_rupiah(order.combo_discount)}",
                f"Order discount: {format_rupiah(order.order_discount)}",
                f"Total: {format_rupiah(order.total)}",
                f"Paid: {format_rupiah(order.amount_paid)}",
                f"Change: {format_rupiah(order.change)}",
                "",
                "Thank you for visiting!",
            ]
        )
        return "\n".join(lines)