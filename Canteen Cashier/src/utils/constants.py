from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MENU_FILE = DATA_DIR / "menu.json"
ORDERS_FILE = DATA_DIR / "orders.json"

APP_NAME = "SynCafe"
WINDOW_BACKGROUND = "#f4f1ec"
CARD_BACKGROUND = "#ffffff"
ACCENT_COLOR = "#79583f"
TEXT_COLOR = "#302a26"
MUTED_COLOR = "#766d65"
