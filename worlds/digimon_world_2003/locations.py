
from .items import ItemData,ALL_ITEMS_TABLE
from typing import Dict, Tuple
from BaseClasses import Location, Region
from dataclasses import dataclass
import json
import importlib
from enum import Enum

class DMW2003FlagType(Enum):
    ITEM_BOX = 0
    STORY = 1
    NPC2 = 2
    QUEST = 3

@dataclass
class DMW2003Flag:
    """flag + flag_type"""
    flag: int
    flag_type: DMW2003FlagType

    def to_key(self) -> int:
        return self.flag_type.value * 1024 + self.flag + 1

class DMW2003Location(Location):
    game: str = "Digimon World 2003"
    
def check_flag(flag_array: bytes, idx: int) -> bool:
    return (flag_array[idx // 8] & (1 << (idx % 8))) > 0 

item_boxes_json_path = importlib.resources.files(__package__).joinpath("item_boxes.json")
with open(item_boxes_json_path, "r") as file:
    item_boxes_json = json.load(file)

ITEM_BOX_LOCATIONS: Dict[str, DMW2003Flag] = {f"Item Box \"{entry["server"]} {entry["name"]} #{entry["i"]}\"": DMW2003Flag(entry["flag"], DMW2003FlagType.ITEM_BOX)  for entry in item_boxes_json}

STORY_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Beat Master Tyrannomon": DMW2003Flag(16, DMW2003FlagType.STORY),
    "Beat Pharaohmon": DMW2003Flag(84, DMW2003FlagType.STORY)
}

NPC2_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Hidden Bits": DMW2003Flag(52, DMW2003FlagType.NPC2),
}

QUEST_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Beat Seiryu Leader": DMW2003Flag(5, DMW2003FlagType.QUEST),
}

ALL_LOCATIONS_TABLE: Dict[str, DMW2003Flag] ={} 
ALL_LOCATIONS_TABLE.update(ITEM_BOX_LOCATIONS)
ALL_LOCATIONS_TABLE.update(STORY_LOCATIONS)
ALL_LOCATIONS_TABLE.update(NPC2_LOCATIONS)
ALL_LOCATIONS_TABLE.update(QUEST_LOCATIONS)

ALL_LOCATIONS_BY_KEY: Dict[int, DMW2003Flag] = {entry.to_key(): entry for (name, entry) in ALL_LOCATIONS_TABLE.items()}

def get_location(name: str, player: int, parent: Region) -> DMW2003Location:
    location = ALL_LOCATIONS_TABLE[name]
    
    return DMW2003Location(player, name, location.to_key(), parent)
