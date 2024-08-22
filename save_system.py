import json
import os
from datetime import datetime, timedelta

SAVE_FILE = "shellmagotchi_save.json"

def save_game(gotchi, last_update_time):
    save_data = {
        "name": gotchi.name,
        "birth_time": gotchi.birth_time.isoformat(),
        "last_update_time": last_update_time,
        "hunger": gotchi.hunger,
        "thirst": gotchi.thirst,
        "sleep": gotchi.sleep,
        "hygiene": gotchi.hygiene,
        "bladder": gotchi.bladder,
        "socialize": gotchi.socialize,
        "happiness": gotchi.happiness,
        "life_stage": gotchi.life_stage.value,
        "alive": gotchi.alive,
        "runaway": gotchi.runaway,
        "dying": gotchi.dying,
        "rebirthing": gotchi.rebirthing,
        "rebirth_signal_sent": gotchi.rebirth_signal_sent,
        "last_update_time": last_update_time
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(save_data, f, indent=2)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None, None
    
    with open(SAVE_FILE, 'r') as f:
        save_data = json.load(f)

    return save_data, float(save_data["last_update_time"])

def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)