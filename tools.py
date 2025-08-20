import json
from typing import Dict, Any

INVENTORY_FILE = "inventory.json"

def load_inventory() -> Dict[str, Any]:
    try:
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_inventory(data: Dict[str, Any]):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_items(item_name: str, quantity: int) -> str:
    inventory = load_inventory()
    if item_name in inventory:
        inventory[item_name] += quantity
    else:
        inventory[item_name] = quantity
    save_inventory(inventory)
    return f"✅ Added {quantity} of {item_name}. Current stock: {inventory[item_name]}"

def delete_items(item_name: str) -> str:
    inventory = load_inventory()
    if item_name in inventory:
        del inventory[item_name]
        save_inventory(inventory)
        return f"🗑️ Deleted {item_name} from inventory."
    return f"❌ Item {item_name} not found."

def update_items(item_name: str, quantity: int) -> str:
    inventory = load_inventory()
    if item_name in inventory:
        inventory[item_name] = quantity
        save_inventory(inventory)
        return f"♻️ Updated {item_name} to {quantity}."
    return f"❌ Item {item_name} not found."