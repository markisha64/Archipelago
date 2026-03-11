
from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Toggle

class FillerItemPool(Choice):
    """Filler items to be added to the Pool."""
    display_name = "Filler Item Pool"
    option_buyable = 0
    option_sellable = 1
    default = 0

class IncludeTamerLocations(Toggle):
    """Include Tamer Locations"""
    display_name = "Tamer Locations"
    default = 1

@dataclass
class DMW2003Options(PerGameCommonOptions):
    filler_item_pool: FillerItemPool
    include_tamer_locations: IncludeTamerLocations
