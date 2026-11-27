#Jefri Handika
import tkinter as tk
from tkinter import ttk

from ..components.item_card import ItemCard


class MenuScreen(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master, padding=24)
        self.app = app
        self.category = tk.StringVar(value="All Categories")
        self.search = tk.StringVar()

        header = ttk.Frame(self)
        header.pack(fill="x")
        ttk.Label(header, text="Menu", style="PageTitle.TLabel").pack(side="left")
        ttk.Button(
            header,
            text="View Cart",
            command=lambda: app.show_screen("Cart"),
        ).pack(side="right")

        filters = ttk.Frame(self)
        filters.pack(fill="x", pady=(14, 12))
        ttk.Label(filters, text="Category").pack(side="left")
        categories = ["All Categories", *sorted({item.category for item in app.menu})]
        category_box = ttk.Combobox(
            filters,
            values=categories,
            textvariable=self.category,
            state="readonly",
            width=18,
        )
        category_box.pack(side="left", padx=(8, 18))
        category_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        ttk.Label(filters, text="Search").pack(side="left")
        search_box = ttk.Entry(filters, textvariable=self.search, width=25)
        search_box.pack(side="left", padx=(8, 0))
        search_box.bind("<KeyRelease>", lambda _event: self.refresh())

        canvas = tk.Canvas(self, highlightthickness=0, bg="#f4f1ec")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.cards_frame = ttk.Frame(canvas)
        self.cards_frame.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        window_id = canvas.create_window(
            (0, 0), window=self.cards_frame, anchor="nw"
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(window_id, width=event.width),
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.refresh()

    def refresh(self) -> None:
        for child in self.cards_frame.winfo_children():
            child.destroy()
        search_text = self.search.get().strip().casefold()
        selected_category = self.category.get()
        items = [
            item for item in self.app.menu
            if (selected_category == "All Categories" or item.category == selected_category)
            and search_text in item.name.casefold()
        ]
        if not items:
            ttk.Label(self.cards_frame, text="No menu items found.").grid(
                row=0, column=0, padx=8, pady=20
            )
        for index, item in enumerate(items):
            ItemCard(
                self.cards_frame,
                item,
                self.app.add_to_cart,
            ).grid(row=index // 3, column=index % 3, padx=7, pady=7, sticky="nsew")
        for column in range(3):
            self.cards_frame.columnconfigure(column, weight=1)