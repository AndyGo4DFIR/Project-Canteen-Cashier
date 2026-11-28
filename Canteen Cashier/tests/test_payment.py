# TIFFANNY
import unittest

from src.models import Payment
from src.utils.money import format_rupiah, parse_amount


class PaymentTests(unittest.TestCase):
    def test_payment_calculates_change(self) -> None:
        payment = Payment(amount_paid=50000, total=32000)
        self.assertEqual(payment.change, 18000)
        self.assertEqual(format_rupiah(payment.change), "Rp18.000")

    def test_payment_rejects_insufficient_amount(self) -> None:
        with self.assertRaises(ValueError):
            Payment(amount_paid=10000, total=32000)

    def test_parse_amount_accepts_rupiah_format(self) -> None:
        self.assertEqual(parse_amount("Rp 125.000"), 125000)
        with self.assertRaises(ValueError):
            parse_amount("invalid")


if __name__ == "__main__":
    unittest.main()