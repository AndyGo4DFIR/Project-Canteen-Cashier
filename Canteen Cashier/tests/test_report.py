# Coder : Endro Delviaro
import tempfile
import unittest

from src.models import Cart, MenuItem
from src.services import OrderService, PricingService, ReportService, StorageService
from src.utils.datetime_helper import today_string

class ReportTests(unittest.TestCase):
    def test_daily_summary_totals_orders_for_the_selected_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            storage = StorageService(directory)
            order_service = OrderService(storage, PricingService())
            cart = Cart()
            cart.add(MenuItem("meal", "Pasta", "Main", 40000))
            order_service.checkout(cart, 40000)

            report = ReportService(order_service.orders).daily_summary(today_string())
            self.assertEqual(report.order_count, 1)
            self.assertEqual(report.items_sold, 1)
            self.assertEqual(report.gross_sales, 40000)
            self.assertEqual(report.net_sales, 40000)

if __name__ == "__main__":
    unittest.main()