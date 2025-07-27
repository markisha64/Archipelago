
from .items import ItemData,ALL_ITEMS_TABLE
from typing import Dict
from BaseClasses import Location

ALL_LOCATIONS_TABLE: Dict[str, ItemData] = {k: v for k, v in ALL_ITEMS_TABLE.items()}

ALL_LOCATIONS_BY_ID: Dict[int, ItemData] = {v.id: v for _, v in ALL_ITEMS_TABLE.items()}

class DMW2003Location(Location):
    game: str = "Digimon World 2003"

def get_location(name: str, player: int) -> DMW2003Location:
    location = ALL_LOCATIONS_TABLE[name]
    
    return DMW2003Location(player, name, location.id)
