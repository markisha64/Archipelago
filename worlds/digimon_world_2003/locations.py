
from .items import ItemData,ALL_ITEMS_TABLE
from typing import Dict, Tuple
from BaseClasses import Location, Region

ALL_LOCATIONS_TABLE: Dict[str, ItemData] = {k: v for k, v in ALL_ITEMS_TABLE.items()}

ALL_LOCATIONS_BY_ID: Dict[int, Tuple[str, ItemData]] = {v.id: (k, v) for k, v in ALL_ITEMS_TABLE.items()}

class DMW2003Location(Location):
    game: str = "Digimon World 2003"

def get_location(name: str, player: int, parent: Region) -> DMW2003Location:
    location = ALL_LOCATIONS_TABLE[name]
    
    return DMW2003Location(player, name, location.id, parent)
