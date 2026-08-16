
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

class PlaceFolderBagEarly(Toggle):
    """Makes it more fun (should play with lower charisma)"""
    display_name = "Place Folder Bag Early"
    default = 1

class IncludeDRILocations(Toggle):
    """Include DRI locations (fight ultimates)"""
    display_name = "DRI Locations"
    default = 1

class IncludeAuctionLocations(Toggle):
    """Include Auction locations"""
    display_name = "Auction Locations"
    default = 1

class PlaceElDoradoIDEarly(Toggle):
    """Makes it more fun (recommended for auctions)"""
    display_name = "Place El Dorado ID Early"
    default = 1

@dataclass
class DMW2003Options(PerGameCommonOptions):
    filler_item_pool: FillerItemPool
    include_tamer_locations: IncludeTamerLocations
    place_folder_bag_early: PlaceFolderBagEarly
    include_dri_locations: IncludeDRILocations
    include_auction_locations: IncludeAuctionLocations
    place_el_dorado_id_early: PlaceElDoradoIDEarly

