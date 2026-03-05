
from typing import Dict
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Item, ItemClassification, Region
from .items import ALL_ITEMS_TABLE,DMW2003Item
from .locations import get_location, ALL_LOCATIONS_TABLE
from .rules import items_owned_rule_gen
from .client import DMW2003Client
from .options import DMW2003Options

class DMW2003WebWorld(WebWorld):
    option_groups = []
    rich_text_options_doc = True
    theme = "grass"
    tutorials = []

class DMW2003World(World):
    origin_region_name = "East Sector"
    game = "Digimon World 2003"
    web = DMW2003WebWorld()
    item_name_to_id = {k: v.id for k, v in ALL_ITEMS_TABLE.items()}
    location_name_to_id = {k: v.to_key() for k, v in ALL_LOCATIONS_TABLE.items()}
    filler_list = [k for k, v in ALL_ITEMS_TABLE.items() if v.classification & ItemClassification.filler != 0]
    region_cache: Dict[int, Region] = {}

    options = DMW2003Options
    options_dataclass = DMW2003Options

    topology_present = True

    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in ALL_ITEMS_TABLE.keys()]

    def create_item(self, name: str) -> Item:
        item = ALL_ITEMS_TABLE[name]

        return DMW2003Item(name, item.classification, item.id, self.player)

    def get_filler_item_name(self):
        return self.random.choice(self.filler_list)

    def create_regions(self):
        east_sector_region = Region("East Sector", self.player, self.multiworld)
        east_sector_region.locations.extend([
            get_location("Hidden Bits", self.player, east_sector_region),
            get_location("Item Box \"Asuka Asuka Sewers #0\"", self.player, east_sector_region),
            get_location("Item Box \"Asuka Central Park #0\"", self.player, east_sector_region),
            get_location("Item Box \"Asuka West Wire Forest #0\"", self.player, east_sector_region),
            get_location("Item Box \"Asuka Divermon's Lake #0\"", self.player, east_sector_region),
            get_location("Beat Master Tyrannomon", self.player, east_sector_region),
            get_location("Beat Pharaohmon", self.player, east_sector_region),
        ])
        self.multiworld.regions.append(east_sector_region)
