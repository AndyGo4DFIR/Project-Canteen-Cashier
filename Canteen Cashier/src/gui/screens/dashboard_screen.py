#Jefri Handika
from tkinter import ttk

from ...utils.datetime_helper import today_string
from ...utils.money import format_rupiah


class DashboardScreen(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master, padding=26)
        summary = app.reports.daily_summary()

        ttk.Label(self, text="Dashboard", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            self,
            text=f"{today_string()} | Welcome to {app.store_name}",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 20))

        cards = ttk.Frame(self)
        cards.pack(fill="x")
        for index, (title, value) in enumerate(
            (
                ("Orders Today", str(summary.order_count)),
                ("Items Sold", str(summary.items_sold)),
                ("Net Sales", format_rupiah(summary.net_sales)),
            )
        ):
            card = ttk.Frame(cards, style="Card.TFrame", padding=18)
            card.grid(row=0, column=index, padx=(0, 12), sticky="nsew")
            cards.columnconfigure(index, weight=1)
            ttk.Label(card, text=title, style="Muted.TLabel").pack(anchor="w")
            ttk.Label(card, text=value, style="Metric.TLabel").pack(
                anchor="w", pady=(8, 0)
            )

        promo_card = ttk.Frame(self, style="Card.TFrame", padding=18)
        promo_card.pack(fill="x", pady=(18, 0))
        ttk.Label(promo_card, text="Combo Deals", style="Section.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            promo_card,
            text=(
                "Pair one Main or Rice Bowl with one Drink and get 10% off the drink. "
                "Each main item can pair with one drink."
            ),
            style="Muted.TLabel",
            wraplength=680,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        ttk.Label(self, text="Start a Sale", style="Section.TLabel").pack(
            anchor="w", pady=(34, 8)
        )
        ttk.Label(
            self,
            text="Choose menu items, review the cart, and complete payment.",
        ).pack(anchor="w")
        ttk.Button(
            self,
            text="Open Menu",
            style="Accent.TButton",
            command=lambda: app.show_screen("Menu"),
        ).pack(anchor="w", pady=14)