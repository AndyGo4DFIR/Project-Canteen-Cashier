# Coder : Endro Delviaro
from datetime import datetime

def current_timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")

def today_string() -> str:
    return datetime.now().astimezone().date().isoformat()

def display_timestamp(value: str) -> str:
    return datetime.fromisoformat(value).astimezone().strftime("%d %b %Y, %H:%M")