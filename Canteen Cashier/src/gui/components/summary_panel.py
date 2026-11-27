#Jefri Handika
from tkinter import ttk

class SummaryPanel(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, style="Card.TFrame", padding=14)
        self.subtotal = ttk.Label(self, text="")
        self.combo_discount = ttk.Label(self, text="")
        self.order_discount = ttk.Label(self, text="")
        self.total = ttk.Label(self, text="", font=("Segoe UI", 13, "bold"))
        for label in (
            self.subtotal,
            self.combo_discount,
            self.order_discount,
            self.total,
        ):
            label.pack(anchor="e", pady=2)

    def refresh(self, quote, format_money) -> None:
        self.subtotal.configure(text=f"Subtotal: {format_money(quote.subtotal)}")
        self.combo_discount.configure(
            text=f"Combo discount: -{format_money(quote.combo_discount)}"
        )
        self.order_discount.configure(
            text=f"Order discount: -{format_money(quote.order_discount)}"
        )
        self.total.configure(text=f"Total: {format_money(quote.total)}")