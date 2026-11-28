# TIFFANNY
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class ReceiptScreen(ttk.Frame):
    def __init__(self, master, app, order) -> None:
        super().__init__(master, padding=24)
        self.receipt_text = app.receipts.render(order, app.store_name)
        ttk.Label(self, text="Receipt", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(
            self,
            text=f"Payment completed | Order {order.id}",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 12))
        text = tk.Text(self, height=20, wrap="none", font=("Consolas", 10))
        text.insert("1.0", self.receipt_text)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Save Receipt", command=self.save_receipt).pack(
            side="left"
        )
        ttk.Button(
            actions,
            text="New Sale",
            style="Accent.TButton",
            command=lambda: app.show_screen("Menu"),
        ).pack(side="right")

    def save_receipt(self) -> None:
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Receipt",
            defaultextension=".txt",
            filetypes=[("Text file", "*.txt")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.receipt_text)
        except OSError as error:
            messagebox.showerror("Save Error", str(error), parent=self)
            return
        messagebox.showinfo("Receipt Saved", "The receipt was saved.", parent=self)