
from .items import ItemData,ALL_ITEMS_TABLE
from typing import Dict, Tuple
from BaseClasses import Location, Region
from dataclasses import dataclass
import json
import importlib

@dataclass
class DMW2003Flag:
    """flag + flag_type"""
    flag: int
    flag_type: str

    def to_key(self) -> str:
        return f"{self.flag_type}_{self.flag}"

class DMW2003Location(Location):
    game: str = "Digimon World 2003"
    
def check_flag(items: bytes, idx: int) -> bool:
    return (items[idx // 8] & (1 << (idx % 8))) > 0 

item_boxes_json_path = importlib.resources.files(__package__).joinpath("item_boxes.json")
with open(item_boxes_json_path, "r") as file:
    item_boxes_json = json.load(file)

ALL_LOCATIONS_TABLE: Dict[str, DMW2003Flag] = {f"{entry["server"]} {entry["name"]} #{entry["i"]}": DMW2003Flag(entry["flag"], "item_box")  for entry in item_boxes_json}
ALL_LOCATIONS_BY_KEY: Dict[str, DMW2003Flag] = {entry.to_key(): entry for (name, entry) in ALL_LOCATIONS_TABLE.items()}

def get_location(name: str, player: int, parent: Region) -> DMW2003Location:
    location = ALL_LOCATIONS_TABLE[name]
    
    return DMW2003Location(player, name, location.id, parent)
