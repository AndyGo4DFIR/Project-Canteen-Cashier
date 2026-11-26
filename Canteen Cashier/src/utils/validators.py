#Coder : Andy
def validate_quantity(quantity: int) -> None:
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("Quantity must be a positive whole number.")
def validate_payment(amount: int, total: int) -> None:
    if isinstance(amount, bool) or not isinstance(amount, int) or amount < total:
        raise ValueError("Payment must be a whole-rupiah amount at least equal to the total.")