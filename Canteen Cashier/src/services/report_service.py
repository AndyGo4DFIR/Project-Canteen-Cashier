# Coder : Endro Delviaro
from ..models import Order, SalesReport
from ..utils.datetime_helper import today_string


class ReportService:
    def __init__(self, orders: list[Order]) -> None:
        self.orders = orders

    def daily_summary(self, date: str | None = None) -> SalesReport:
        report_date = date or today_string()
        day_orders = [
            order for order in self.orders
            if order.created_at[:10] == report_date
        ]
        return SalesReport(
            date=report_date,
            order_count=len(day_orders),
            items_sold=sum(
                item["quantity"]
                for order in day_orders
                for item in order.items
            ),
            gross_sales=sum(order.subtotal for order in day_orders),
            discounts=sum(
                order.combo_discount + order.order_discount
                for order in day_orders
            ),
            net_sales=sum(order.total for order in day_orders),
        )