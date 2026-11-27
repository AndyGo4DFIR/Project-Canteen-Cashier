from tkinter import ttk

from ...utils.money import format_rupiah


class ItemCard(ttk.Frame):
    def __init__(self, master, menu_item, on_add) -> None:
        super().__init__(master, padding=14, style="Card.TFrame")
        ttk.Label(
            self,
            text=menu_item.name,
            font=("Segoe UI", 11, "bold"),
            wraplength=190,
        ).pack(anchor="w")
        ttk.Label(
            self,
            text=menu_item.category,
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 6))
        ttk.Label(
            self,
            text=format_rupiah(menu_item.price),
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(0, 10))
        ttk.Button(
            self,
            text="Add to Cart",
            command=lambda: on_add(menu_item),
        ).pack(fill="x")