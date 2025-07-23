
from .items import ItemData,ALL_ITEMS_TABLE
from typing import Dict
from BaseClasses import Location

ALL_LOCATION_TABLE: Dict[str, ItemData] = ALL_ITEMS_TABLE

def get_location(name: str, player: int):
    location = ALL_LOCATION_TABLE[name]
    
    return Location(player, name, location.id)
