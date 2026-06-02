import json
import os

MEMORY_FILE = "user_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_user_profile(user_id: str, profile: dict):
    memory = load_memory()
    memory[user_id] = profile
    save_memory(memory)

def get_user_profile(user_id: str):
    memory = load_memory()
    return memory.get(user_id, None)