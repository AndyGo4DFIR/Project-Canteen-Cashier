#Jefri Handika
from tkinter import ttk

from ...utils.money import format_rupiah


class CartTable(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.table = ttk.Treeview(
            self,
            columns=("name", "quantity", "price", "total"),
            show="headings",
            selectmode="browse",
            height=10,
        )
        for column, title, width in (
            ("name", "Item", 290),
            ("quantity", "Qty", 70),
            ("price", "Price", 140),
            ("total", "Line Total", 150),
        ):
            self.table.heading(column, text=title)
            self.table.column(
                column,
                width=width,
                anchor="w" if column == "name" else "e",
            )
        self.table.pack(fill="both", expand=True)

    def refresh(self, cart) -> None:
        self.table.delete(*self.table.get_children())
        for item in cart.items:
            self.table.insert(
                "",
                "end",
                iid=item.menu_item.id,
                values=(
                    item.menu_item.name,
                    item.quantity,
                    format_rupiah(item.menu_item.price),
                    format_rupiah(item.line_total),
                ),
            )

    def selected_item_id(self) -> str | None:
        selected = self.table.selection()
        return selected[0] if selected else None