import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from ...utils.datetime_helper import today_string
from ...utils.money import format_rupiah


class SummaryScreen(ttk.Frame):
    def __init__(self, master, app) -> None:
        super().__init__(master, padding=24)
        self.app = app
        ttk.Label(self, text="Daily Sales Summary", style="PageTitle.TLabel").pack(
            anchor="w"
        )
        controls = ttk.Frame(self)
        controls.pack(anchor="w", pady=(12, 14))
        self.report_date = tk.StringVar(value=today_string())
        ttk.Label(controls, text="Date (YYYY-MM-DD)").pack(side="left")
        ttk.Entry(controls, textvariable=self.report_date, width=13).pack(
            side="left", padx=(8, 8)
        )
        ttk.Button(controls, text="Show Summary", command=self.refresh).pack(side="left")
        self.summary_text = ttk.Label(self, text="", style="Section.TLabel")
        self.summary_text.pack(anchor="w", pady=(0, 16))
        self.refresh()

    def refresh(self) -> None:
        date_text = self.report_date.get().strip()
        try:
            date.fromisoformat(date_text)
            report = self.app.reports.daily_summary(date_text)
        except ValueError as error:
            messagebox.showerror("Invalid Date", str(error), parent=self)
            return
        self.summary_text.configure(
            text=(
                f"Orders: {report.order_count}\n"
                f"Items sold: {report.items_sold}\n"
                f"Gross sales: {format_rupiah(report.gross_sales)}\n"
                f"Discounts: {format_rupiah(report.discounts)}\n"
                f"Net sales: {format_rupiah(report.net_sales)}"
            )
        )