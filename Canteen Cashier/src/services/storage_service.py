# ERIC
import json
from pathlib import Path

from ..models import MenuItem, Order
from ..utils.constants import MENU_FILE, ORDERS_FILE


class StorageService:
    def __init__(self, data_dir: Path | str | None = None) -> None:
        self.data_dir = Path(data_dir) if data_dir else MENU_FILE.parent
        self.menu_file = self.data_dir / MENU_FILE.name
        self.orders_file = self.data_dir / ORDERS_FILE.name
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _read_json(path: Path, default):
        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _write_json(path: Path, data) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temporary.replace(path)

    def load_menu(self) -> list[MenuItem]:
        rows = self._read_json(self.menu_file, [])
        if not rows:
            raise ValueError(f"Menu file is empty: {self.menu_file}")
        items = [MenuItem.from_dict(row) for row in rows]
        if len({item.id for item in items}) != len(items):
            raise ValueError("Menu item IDs must be unique.")
        return items

    def load_orders(self) -> list[Order]:
        return [
            Order.from_dict(row)
            for row in self._read_json(self.orders_file, [])
        ]

    def save_orders(self, orders: list[Order]) -> None:
        self._write_json(self.orders_file, [order.to_dict() for order in orders])
