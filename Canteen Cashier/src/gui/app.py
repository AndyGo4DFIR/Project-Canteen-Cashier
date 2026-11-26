# ERIC
import tkinter as tk
from tkinter import ttk

from ..models import Cart
from ..services import (
    OrderService,
    PricingService,
    ReceiptService,
    ReportService,
    StorageService,
)
from ..utils.constants import (
    ACCENT_COLOR,
    APP_NAME,
    CARD_BACKGROUND,
    MUTED_COLOR,
    TEXT_COLOR,
    WINDOW_BACKGROUND,
)
from .screens.cart_screen import CartScreen
from .screens.dashboard_screen import DashboardScreen
from .screens.menu_screen import MenuScreen
from .screens.payment_screen import PaymentScreen
from .screens.receipt_screen import ReceiptScreen
from .screens.summary_screen import SummaryScreen


class CashierApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME} | Canteen Cashier")
        self.geometry("1060x700")
        self.minsize(900, 600)
        self.configure(background=WINDOW_BACKGROUND)

        self.storage = StorageService()
        self.menu = self.storage.load_menu()
        self.cart = Cart()
        self.pricing = PricingService()
        self.orders = OrderService(self.storage, self.pricing)
        self.reports = ReportService(self.orders.orders)
        self.receipts = ReceiptService()
        self.store_name = APP_NAME
        self.current_screen = None
        self.current_screen_name = "Dashboard"
        self.navigation: dict[str, ttk.Button] = {}

        self._configure_styles()
        self._build_layout()
        self.show_screen("Dashboard")

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10), foreground=TEXT_COLOR)
        style.configure("TFrame", background=WINDOW_BACKGROUND)
        style.configure("Card.TFrame", background=CARD_BACKGROUND)
        style.configure("PageTitle.TLabel", font=("Segoe UI", 21, "bold"))
        style.configure("Section.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure(
            "Metric.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground=ACCENT_COLOR,
        )
        style.configure("Muted.TLabel", foreground=MUTED_COLOR)
        style.configure(
            "Accent.TButton",
            background=ACCENT_COLOR,
            foreground="#ffffff",
            padding=(12, 8),
        )
        style.map("Accent.TButton", background=[("active", "#62442f")])
        style.configure("Treeview", rowheight=30, background="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_layout(self) -> None:
        header = tk.Frame(self, bg="#ffffff", height=62)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="SynCafe",
            bg="#ffffff",
            fg=ACCENT_COLOR,
            font=("Segoe UI", 19, "bold"),
        ).pack(side="left", padx=22)
        tk.Label(
            header,
            text="Canteen Cashier",
            bg="#ffffff",
            fg=MUTED_COLOR,
            font=("Segoe UI", 10),
        ).pack(side="right", padx=22)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)
        sidebar = tk.Frame(body, bg="#ffffff", width=185)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        for name in ("Dashboard", "Menu", "Cart", "Daily Summary"):
            button = ttk.Button(
                sidebar,
                text=name,
                command=lambda selected=name: self.show_screen(selected),
            )
            button.pack(fill="x", padx=10, pady=4)
            self.navigation[name] = button

        self.content = ttk.Frame(body)
        self.content.pack(side="left", fill="both", expand=True)
        self.status = tk.StringVar(value="Ready")
        tk.Label(
            self,
            textvariable=self.status,
            anchor="w",
            bg="#ffffff",
            fg=MUTED_COLOR,
            padx=12,
            pady=6,
        ).pack(fill="x", side="bottom")

    def show_screen(self, name: str) -> None:
        screens = {
            "Dashboard": DashboardScreen,
            "Menu": MenuScreen,
            "Cart": CartScreen,
            "Daily Summary": SummaryScreen,
        }
        if name not in screens:
            raise ValueError(f"Unknown screen: {name}")
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.current_screen = screens[name](self.content, self)
        self.current_screen.pack(fill="both", expand=True)
        self.current_screen_name = name
        for button_name, button in self.navigation.items():
            button.state(["pressed"] if button_name == name else ["!pressed"])

    def refresh_screen(self) -> None:
        self.show_screen(self.current_screen_name)

    def add_to_cart(self, menu_item) -> None:
        self.cart.add(menu_item)
        self.status.set(f"{menu_item.name} added to cart")
        self.refresh_screen()

    def open_payment(self) -> None:
        if self.cart.is_empty:
            from tkinter import messagebox

            messagebox.showinfo("Cart", "Add at least one item first.", parent=self)
            return
        PaymentScreen(self, self)

    def complete_payment(self, amount_paid: int) -> None:
        order = self.orders.checkout(self.cart, amount_paid)
        self.status.set(f"Payment completed | Order {order.id}")
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.current_screen = ReceiptScreen(self.content, self, order)
        self.current_screen.pack(fill="both", expand=True)
        self.current_screen_name = "Receipt"
