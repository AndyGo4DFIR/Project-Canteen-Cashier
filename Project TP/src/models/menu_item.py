import re
from dataclasses import dataclass
from decimal import Decimal
from src.utils.validators import validate_money
@dataclass(frozen=True)
class MenuItem:
  item_id: str
  name: str
  price: Decimal
  category: str = "general"
  def __post_init__(self):
    if not self.item_id.strip():
      raise ValueError("item_id is required")
    if not self.name.strip():
      raise ValueError("name is required")
    object.__setattr__(self, "price", validate_money(self.price, "price"))
FOOD="Makanan Berat"
COFFEE="Drinks/Coffee"
NON_COFFEE="Drinks/Non-Coffee"
JUICE="Drinks/Juice"
DESSERT="Dessert"
def _slug(text: str)->str:
  return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
def _build()-> list[MenuItem]:
  items: list[MenuItem]=[]
  def add(category,name,price,group=None):
    full_name=f"{group} - {name}" if group else name
    items.append(MenuItem(f"{_slug(category)}-{_slug(full_name)}", full_name,price, category))
  def add_all(category, pairs, group=None):
    for name, price in pairs:
      add(category, name, price, group)
  def add_same_price(category, group, names, price):
    for name in names:
      add(category, name, price, group)
# FOOD
  add_same_price(FOOD, "Spaghetti",
        ["Carbonara", "Bolognese", "Mushroom", "Aglio e Olio"],
        "35000",
  )
  add_same_price(FOOD, "Rice Bowl",
        ["Chicken Katsu", "Crispy Chicken", "Chicken Salted Egg",
        "Chicken Curry", "Chicken Blackpepper", "Chicken Teriyaki"],
        "35000",
  )
  add_all(FOOD,[
    ("Fried Rice", "25000"),
    ("Chicken Carbonara", "32000"),
    ("Salted Egg Curry Chicken", "60000"),
  ])
  add_all(FOOD, [
    ("Grilled Chicken", "30000"),
    ("Grilled Beef", "45000"),
    ("Crispy Chicken", "30000"),
    ("Chicken Patties", "28000"),
  ], group="Steak")
#Drinks
  add_all(COFFEE, [
    ("Syntech Latte", "50000"),
    ("Americano", "30000"),
    ("Espresso", "25000"),
    ("Latte", "32000"),
    ("Butterscotch", "35000"),
    ("Spanish Latte", "35000"),
    ("Cappuccino", "32000"),
    ("Black Aren Latte", "35000"),
    ("Caramel Latte", "35000"),
    ("Creamy Aren Latte", "35000"),
    ("Matcha Latte", "40000"),
    ("Chocolate Latte", "40000"),
  ])
  add_all(NON_COFFEE, [
    ("Thai Tea", "28000"),
    ("Green Tea", "25000"),
    ("Lychee Tea", "25000"),
    ("Fresh Lemonade", "18000"),
    ("Oolong Tea", "15000"),
    ("Lemon Tea", "15000"),
  ])
  add_all(JUICE, [
    ("Avocado Juice", "45000"),
    ("Sirsak Juice", "40000"),
    ("Tomato Juice", "30000"),
    ("Carrot Juice", "30000"),
    ("Orange Juice", "30000"),
    ("Lychee Juice", "30000"),
    ("Dragon Juice", "45000"),
    ("Mango Juice", "30000"),
    ("Melon Juice", "30000"),
    ("Strawberry Juice", "30000"),
    ("Grape Juice", "30000"),
  ])
  add_all(DESSERT, [
    ("Vanilla", "10000"),
    ("Chocolate", "10000"),
    ("Matcha", "10000"),
    ("Syntech", "12000"),
  ], group="Ice Cream")
  add_all(DESSERT, [
    ("Syntech", "40000"),
    ("Cheese", "35000"),
    ("Choco", "35000"),
    ("Strawberry", "35000"),
  ], group="Cakes")
  add(DESSERT, "French Fries", "20000")
  add_same_price(DESSERT, "Donuts", ["Cheese", "Matcha", "Greentea", "Chocolate"], "20000")
  add_all(DESSERT, [("Cookies", "30000"), ("Pancake", "25000")])
  add_all(DESSERT, [
    ("Chocolatte", "28000"),
    ("Strawberry", "28000"),
    ("Nutella", "30000"),
    ("Oreo", "28000"),
    ("Cheese", "30000"),
  ], group="Waffle")
  ids = [i.item_id for i in items]
  if len(ids)!=len(set(ids)):
    raise ValueError("Duplicate menu item_id found")
  return items
MENU: list[MenuItem]= _build()
MENU_BY_ID: dict[str, MenuItem]={i.item_id: i for i in MENU}
def get_item(item_id: str)->MenuItem:
  try:
    return MENU_BY_ID[item_id]
  except KeyError:
    raise ValueError(f"Unknown menu item: {item_id}") from None
def items_in(category: str)->list[MenuItem]:
  return [i for i in MENU if i.category == category]