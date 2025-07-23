
from .items import ItemData,ALL_ITEMS_TABLE
from typing import Dict
from BaseClasses import Location,ItemClassification

ALL_LOCATIONS_TABLE: Dict[str, ItemData] = {k: v for k, v in ALL_ITEMS_TABLE.items()}

ALL_LOCATIONS_TABLE["Beat Galacticmon"] = ItemData(6464, ItemClassification.progression)

def get_location(name: str, player: int):
    location = ALL_LOCATIONS_TABLE[name]
    
    return Location(player, name, location.id)
