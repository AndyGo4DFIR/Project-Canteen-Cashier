from dataclasses import dataclass


@dataclass(frozen=True)
class SalesReport:
    date: str
    order_count: int
    items_sold: int
    gross_sales: int
    discounts: int
    net_sales: int