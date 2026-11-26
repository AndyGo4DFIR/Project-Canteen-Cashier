#Coder : Andy
def format_rupiah(amount: int) -> str:
    return f"Rp{amount:,}".replace(",", ".")
def parse_amount(value: str) -> int:
    cleaned = value.strip().replace("Rp", "").replace("rp", "")
    cleaned = cleaned.replace(".", "").replace(",", "").replace(" ", "")
    if not cleaned.isdigit():
        raise ValueError("Enter a valid whole-rupiah amount.")
    return int(cleaned)