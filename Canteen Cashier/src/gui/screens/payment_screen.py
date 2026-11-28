# TIFFANNY
import tkinter as tk
from tkinter import messagebox, ttk

from ...utils.money import format_rupiah, parse_amount
from ..components.summary_panel import SummaryPanel


class PaymentScreen(tk.Toplevel):
    def __init__(self, parent, app) -> None:
        super().__init__(parent)
        self.app = app
        self.title("Payment")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.quote = app.pricing.calculate(app.cart)
        self.cash_input = tk.StringVar()
        self.change_text = tk.StringVar(value=format_rupiah(0))

        body = ttk.Frame(self, padding=22)
        body.pack(fill="both", expand=True)
        ttk.Label(body, text="Payment", style="PageTitle.TLabel").pack(anchor="w")
        self.summary = SummaryPanel(body)
        self.summary.pack(fill="x", pady=(12, 18))
        self.summary.refresh(self.quote, format_rupiah)

        ttk.Label(body, text="Cash Received").pack(anchor="w")
        entry = ttk.Entry(body, textvariable=self.cash_input, width=30)
        entry.pack(fill="x", pady=(5, 12))
        entry.bind("<KeyRelease>", self.update_change)
        ttk.Label(body, text="Change").pack(anchor="w")
        ttk.Label(body, textvariable=self.change_text, style="Metric.TLabel").pack(
            anchor="w", pady=(4, 16)
        )

        buttons = ttk.Frame(body)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Back", command=self.destroy).pack(side="right")
        ttk.Button(
            buttons,
            text="Complete Payment",
            style="Accent.TButton",
            command=self.confirm_payment,
        ).pack(side="right", padx=(0, 8))
        entry.focus_set()
        self.bind("<Return>", lambda _event: self.confirm_payment())

    def update_change(self, _event=None) -> None:
        try:
            amount = parse_amount(self.cash_input.get())
            self.change_text.set(format_rupiah(max(0, amount - self.quote.total)))
        except ValueError:
            self.change_text.set(format_rupiah(0))

    def confirm_payment(self) -> None:
        try:
            amount = parse_amount(self.cash_input.get())
            self.app.complete_payment(amount)
        except (ValueError, OSError) as error:
            messagebox.showerror("Payment Error", str(error), parent=self)
            return
        self.destroy()