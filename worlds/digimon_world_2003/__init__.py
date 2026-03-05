
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
        items_owned_rule = items_owned_rule_gen(self.player)
        
        east_sector_region = Region("East Sector", self.player, self.multiworld)
        east_sector_region.locations.extend([
            get_location("Hidden Bits", self.player, east_sector_region),
            get_location("Item Box \"Asuka Asuka Sewers #0\"", self.player, east_sector_region),
            get_location("Item Box \"Asuka Central Park #0\"", self.player, east_sector_region),
            get_location("Item Box \"Asuka West Wire Forest #0\"", self.player, east_sector_region),
            get_location("Item Box \"Asuka Divermon's Lake #0\"", self.player, east_sector_region),
            get_location("Beat Master Tyrannomon", self.player, east_sector_region),
            get_location("Beat Pharaohmon", self.player, east_sector_region),
            get_location("Beat Seiryu Leader", self.player, east_sector_region),
            # keith is questionable since hes missable
            get_location("Beat Keith", self.player, east_sector_region),
        ])

        south_sector_1_region = Region("South Sector I", self.player, self.multiworld)
        east_sector_region.connect(south_sector_1_region, "Blue Card", items_owned_rule(["Blue Card"]))
        south_sector_1_region.locations.extend([
            get_location("Item Box \"Asuka Bulk Bridge #0\"", self.player, south_sector_1_region),
        ])

        south_sector_2_region = Region("South Sector II", self.player, self.multiworld)
        south_sector_1_region.connect(south_sector_2_region, "Sepik Mask", items_owned_rule(["Sepik Mask"]))
        south_sector_2_region.locations.extend([
            get_location("Item Box \"Asuka Jungle Shrine #0\"", self.player, south_sector_2_region),
            # also questionable
            get_location("Item Box \"Asuka Admin Center 2F #0\"", self.player, south_sector_2_region),
            get_location("Beat Suzaku Leader", self.player, south_sector_2_region),
            get_location("Beat Zanbamon", self.player, south_sector_2_region),
        ])

        west_sector_region  = Region("Reliability Spot", self.player, self.multiworld)
        south_sector_2_region.connect(west_sector_region , "TNT Chip", items_owned_rule(["TNT Chip"]))

        west_sector_region.locations.extend([
            get_location("DE Sincerity", self.player, west_sector_region),
            get_location("Item Box \"Asuka Suzaku UG Lake #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Asuka Sewers #1\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka North Badland W #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka North Badland W #1\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka North Badland W #2\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka North Badland E #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Duct Room 01 #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Duct Room 02 #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Duct Room 03 #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Duct Room 04 #0\"", self.player, west_sector_region),
            get_location("Beat Fake Byakko Leader", self.player, west_sector_region),
            get_location("Beat Byakko Leader", self.player, west_sector_region),
            get_location("Beat HiAndromon", self.player, west_sector_region),
            # TODO: decide if I want to add WaruMonzaemon and Ambusher
            get_location("Beat Datamon", self.player, west_sector_region),
        ])

        self.multiworld.regions.extend([
            east_sector_region,
            south_sector_1_region,
            south_sector_2_region,
            west_sector_region
        ])
