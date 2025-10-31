import json
import os

DATA_FILE = 'guest.json'

def load_guests():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_guest(guest):
    guests = load_guests()
    guests.append(guest)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(guests, f, ensure_ascii=False, indent=2)
