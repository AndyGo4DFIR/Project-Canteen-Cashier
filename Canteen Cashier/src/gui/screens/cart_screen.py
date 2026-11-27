from tkinter import messagebox, ttk

from ...utils.money import format_rupiah
from ..components.cart_table import CartTable
from ..components.summary_panel import SummaryPanel


class CartScreen(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master, padding=24)
        self.app = app
        ttk.Label(self, text="Cart", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            self,
            text="Select a row and remove one unit, or clear the cart.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 14))

        self.table = CartTable(self)
        self.table.pack(fill="both", expand=True)
        self.summary = SummaryPanel(self)
        self.summary.pack(fill="x", pady=(12, 8))

        buttons = ttk.Frame(self)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Remove One", command=self.remove_one).pack(side="left")
        ttk.Button(buttons, text="Clear Cart", command=self.clear_cart).pack(
            side="left", padx=8
        )
        ttk.Button(
            buttons,
            text="Continue to Payment",
            style="Accent.TButton",
            command=app.open_payment,
        ).pack(side="right")
        self.refresh()

    def refresh(self) -> None:
        self.table.refresh(self.app.cart)
        self.summary.refresh(
            self.app.pricing.calculate(self.app.cart),
            format_rupiah,
        )

    def remove_one(self) -> None:
        item_id = self.table.selected_item_id()
        if item_id is None:
            messagebox.showinfo("Cart", "Select an item first.", parent=self)
            return
        self.app.cart.remove_one(item_id)
        self.app.refresh_screen()

    def clear_cart(self) -> None:
        if self.app.cart.is_empty:
            return
        if messagebox.askyesno("Clear Cart", "Remove all items?", parent=self):
            self.app.cart.clear()
            self.app.refresh_screen()