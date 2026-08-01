
from typing import Dict
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Item, ItemClassification, Region, Tutorial
from .items import NON_FILLER,NON_BUYABLE_FILLER, BUYABLE_FILLER,DMW2003Item,ALL_ITEMS_TABLE
from .locations import get_location, ALL_LOCATIONS_TABLE
from .rules import items_owned_rule_gen
from .client import DMW2003Client
from .options import DMW2003Options

class DMW2003WebWorld(WebWorld):
    option_groups = []
    rich_text_options_doc = True
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing Digimon World 2003 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["markisha64"]
    )
    tutorials = [setup_en]

class DMW2003World(World):
    origin_region_name = "East Sector"
    game = "Digimon World 2003"
    web = DMW2003WebWorld()
    item_name_to_id = {k: v.id for k, v in ALL_ITEMS_TABLE.items()}
    location_name_to_id = {k: v.to_key() for k, v in ALL_LOCATIONS_TABLE.items()}
    filler_list = [k for k, v in ALL_ITEMS_TABLE.items() if v.classification == ItemClassification.filler]
    region_cache: Dict[int, Region] = {}

    options: DMW2003Options
    options_dataclass = DMW2003Options

    topology_present = True

    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in NON_FILLER.keys()]

        self.multiworld.itempool += [self.create_item(name) for name in BUYABLE_FILLER.keys()]

        # if option sellable
        if self.options.filler_item_pool.value == 1:
            self.multiworld.itempool += [self.create_item(name) for name in NON_BUYABLE_FILLER.keys()]

        # game softlocks if you try training without Silver ID after East Sector
        self.multiworld.get_location("Beat Seiryu Leader", self.player).place_locked_item(self.create_item("Silver ID"))

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

        west_sector_region = Region("West Sector", self.player, self.multiworld)
        south_sector_2_region.connect(west_sector_region , "TNT Chip", items_owned_rule(["TNT Chip"]))

        west_sector_region.locations.extend([
            get_location("DE Sincerity", self.player, west_sector_region),
            get_location("Item Box \"Asuka Suzaku UG Lake #0\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Asuka Sewers #1\"", self.player, west_sector_region),
            get_location("Item Box \"Asuka Asuka Bridge #0\"", self.player, west_sector_region),
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

        amaterasu_region = Region("Amaterasu", self.player, self.multiworld)
        west_sector_region.connect(amaterasu_region, "Staff Pass", items_owned_rule(["Staff Pass"]))
        amaterasu_region.locations.extend([
            # AS Admin Center
            get_location("Item Box \"Asuka Admin Center 1F #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Admin Center B1F #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Admin Center B1F #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Admin Center B1F #2\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Asuka City #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Asuka City #1\"", self.player, amaterasu_region),
            # Bug Maze
            get_location("Item Box \"Asuka Bug Maze #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Bug Maze #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Bug Maze #2\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Bug Maze Pit #0\"", self.player, amaterasu_region),
            # AM Pre DE Knowledge
            get_location("Beat BK MegaGargomon", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Divermon's Lake #0\"", self.player, amaterasu_region),
            get_location("Beat BK Imperialdramon", self.player, amaterasu_region),
            get_location("Beat Qing Long Chief", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Central Park #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Jungle Shrine #0\"", self.player, amaterasu_region),
            get_location("Beat Zhu Que Chief", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Zhu Que UG Lake #0\"", self.player, amaterasu_region),
            get_location("DE Knowledge", self.player, amaterasu_region),
            # AM West Sector
            get_location("Item Box \"Amaterasu North Badland W #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu North Badland W #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Duct Room 01 #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Duct Room 02 #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Duct Room 03 #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Duct Room 04 #0\"", self.player, amaterasu_region),
            get_location("Beat BK WarGrowlmon", self.player, amaterasu_region),
            get_location("Beat BK KingNumemon", self.player, amaterasu_region),
            get_location("Beat Bai Hu Chief", self.player, amaterasu_region),
            # AS North Sector
            get_location("Item Box \"Asuka Boot Mountain #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Boot Mountain #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Snow Mountain #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Snow Mountain #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Freeze Mountain #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Freeze Mountain #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Dark Dungeon #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Genbu City #0\"", self.player, amaterasu_region),
            get_location("Beat Genbu Leader", self.player, amaterasu_region),
            get_location("Beat Ice Witch", self.player, amaterasu_region),
            get_location("Beat Fire Knight", self.player, amaterasu_region),
            get_location("Beat Dark Knight", self.player, amaterasu_region),
            # AM North Sector
            get_location("Item Box \"Amaterasu Boot Mountain #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Freeze Mountain #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Dark Dungeon #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Xuan Wu City #0\"", self.player, amaterasu_region),
            get_location("Beat Xuan Wu Chief", self.player, amaterasu_region),
            get_location("Beat Ice Master", self.player, amaterasu_region),
            get_location("Beat Fire Master", self.player, amaterasu_region),
            get_location("Beat Dark Master", self.player, amaterasu_region),
            # Amaterasu City
            get_location("Item Box \"Amaterasu Amaterasu Sewer #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Amaterasu Sewer #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Amaterasu Bridge #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Admin Center 1F #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Admin Center B1F #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Admin Center B1F #1\"", self.player, amaterasu_region),
            # empty box
            # get_location("Item Box \"Amaterasu Admin Center B1F #2\"", self.player, amaterasu_region), 
            # get_location("Item Box \"Asuka Admin Center 2F #0\"", self.player, south_sector_2_region),
            # Digmon only boxes
            get_location("Item Box \"Asuka Kicking Forest #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Kicking Forest #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Wind Prairie #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Wind Prairie #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Pelche Oasis #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Amaterasu Pelche Oasis #0\"", self.player, amaterasu_region),
            # Magasta B1F (commented empty boxes)
            get_location("Item Box \"Asuka Magasta B1F #0\"", self.player, amaterasu_region),
            # get_location("Item Box \"Asuka Magasta B1F #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B1F #2\"", self.player, amaterasu_region),
            # get_location("Item Box \"Asuka Magasta B1F #3\"", self.player, amaterasu_region),
            # get_location("Item Box \"Asuka Magasta B1F #4\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B1F #5\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B1F #6\"", self.player, amaterasu_region),
            # get_location("Item Box \"Asuka Magasta B1F #7\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B1F #8\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B1F #9\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B1F #10\"", self.player, amaterasu_region),
            # Magasta B2F (commented empty boxes)
            get_location("Item Box \"Asuka Magasta B2F #0\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B2F #1\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B2F #2\"", self.player, amaterasu_region),
            # get_location("Item Box \"Asuka Magasta B2F #3\"", self.player, amaterasu_region),
            get_location("Item Box \"Asuka Magasta B2F #4\"", self.player, amaterasu_region),
        ])

        self.multiworld.regions.extend([
            east_sector_region,
            south_sector_1_region,
            south_sector_2_region,
            west_sector_region,
            amaterasu_region,
        ])

        if self.options.include_tamer_locations.value == 1:
            self.create_tamer_regions()

        if self.options.include_dri_locations.value == 1:
            self.create_dri_regions()

    def create_dri_regions(self):
        west_sector_region = self.get_region("West Sector")
        west_sector_region.locations.extend([
            get_location("MetalGreymon", self.player, west_sector_region),
            get_location("Armormon", self.player, west_sector_region),
            get_location("Paildramon", self.player, west_sector_region),
            get_location("WarGrowlmon", self.player, west_sector_region),
            get_location("MagnaAngemon", self.player, west_sector_region),
            get_location("Taomon", self.player, west_sector_region),
            get_location("Kyukimon", self.player, west_sector_region),
            get_location("GrapLeomon", self.player, west_sector_region),
        ])

    def create_tamer_regions(self):
        items_owned_rule = items_owned_rule_gen(self.player)

        east_sector_region = self.get_region("East Sector")
        south_sector_1_region = self.get_region("South Sector I")
        south_sector_2_region = self.get_region("South Sector II")
        west_sector_region = self.get_region("West Sector")
        amaterasu_region = self.get_region("Amaterasu")

        east_sector_tamers_region = Region("East Sector Tamers", self.player, self.multiworld)
        east_sector_region.connect(east_sector_tamers_region, "East Sector + Folder Bag", items_owned_rule(["Folder Bag"]))
        east_sector_tamers_region.locations.extend([
            get_location("Tamer Natsumi", self.player, east_sector_tamers_region),
            get_location("Tamer Genji", self.player, east_sector_tamers_region),
            get_location("Tamer Catherine", self.player, east_sector_tamers_region),
            get_location("Tamer Lucia", self.player, east_sector_tamers_region),
            get_location("Tamer Robert", self.player, east_sector_tamers_region),
            get_location("Tamer Akiba", self.player, east_sector_tamers_region),
            get_location("Tamer Tomomi", self.player, east_sector_tamers_region),
            get_location("Tamer Chris", self.player, east_sector_tamers_region),
        ])

        east_sector_legy_tamers_region = Region("East Sector Legendary Tamers", self.player, self.multiworld)
        east_sector_tamers_region.connect(east_sector_legy_tamers_region, "East Sector + Folder Bag + Asuka Trophy", items_owned_rule(["Asuka Trophy"]))
        east_sector_legy_tamers_region.locations.extend([
            get_location("Tamer Mitch", self.player, east_sector_legy_tamers_region),  
            get_location("Tamer Bob", self.player, east_sector_legy_tamers_region),  
        ])

        south_sector_1_tamers_region = Region("South Sector I Tamers", self.player, self.multiworld)
        south_sector_1_region.connect(south_sector_1_tamers_region, "South Sector I + Folder Bag", items_owned_rule(["Folder Bag"]))
        south_sector_1_tamers_region.locations.extend([
            get_location("Tamer Andy", self.player, south_sector_1_tamers_region),
            get_location("Tamer George", self.player, south_sector_1_tamers_region),
            get_location("Tamer Mei Lin", self.player, south_sector_1_tamers_region),
        ])

        south_sector_1_legy_tamers_region = Region("South Sector I Legendary Tamers", self.player, self.multiworld)
        south_sector_1_tamers_region.connect(south_sector_1_legy_tamers_region, "South Sector I + Folder Bag + Asuka Trophy", items_owned_rule(["Asuka Trophy"]))
        south_sector_1_legy_tamers_region.locations.extend([
            get_location("Tamer Jessica", self.player, south_sector_1_legy_tamers_region),
        ])

        south_sector_2_tamers_region = Region("South Sector II Tamers", self.player, self.multiworld)
        south_sector_2_region.connect(south_sector_2_tamers_region, "South Sector II + Folder Bag", items_owned_rule(["Folder Bag"]))
        south_sector_2_tamers_region.locations.extend([
            get_location("Tamer Gordon", self.player, south_sector_2_tamers_region),
            get_location("Tamer Alice", self.player, south_sector_2_tamers_region),
        ])

        west_sector_tamers_region = Region("West Sector Tamers", self.player, self.multiworld)
        west_sector_region.connect(west_sector_tamers_region, "West Sector + Folder Bag + Asuka Trophy", items_owned_rule([
            "Folder Bag",
            "Asuka Trophy"
        ]))
        west_sector_tamers_region.locations.extend([
            get_location("Tamer Nakano", self.player, west_sector_tamers_region)
        ])

        north_sector_tamers_region = Region("North Sector Tamers", self.player, self.multiworld)
        amaterasu_region.connect(north_sector_tamers_region, "North Sector + Folder Bag", items_owned_rule([
           "Folder Bag",
        ]))
        north_sector_tamers_region.locations.extend([
            get_location("Tamer Brown", self.player, north_sector_tamers_region),
        ])
    
        north_sector_legy_tamers_s_region = Region("North Sector Legendary Tamers S", self.player, self.multiworld)
        north_sector_tamers_region.connect(north_sector_legy_tamers_s_region, "North Sector + Folder Bag + Sun Trophy", items_owned_rule([
           "Sun Trophy",
        ]))
        north_sector_legy_tamers_s_region.locations.extend([
            get_location("Tamer Haruka", self.player, north_sector_legy_tamers_s_region),
            get_location("Tamer Poemy", self.player, north_sector_legy_tamers_s_region),
            get_location("Tamer Pierre", self.player, north_sector_legy_tamers_s_region),
            get_location("Tamer Shingo", self.player, north_sector_legy_tamers_s_region),
            get_location("Tamer Makoto", self.player, north_sector_legy_tamers_s_region),
        ])

        north_sector_legy_tamers_a_region = Region("North Sector Legendary Tamers A", self.player, self.multiworld)
        north_sector_tamers_region.connect(north_sector_legy_tamers_a_region, "North Sector + Folder Bag + Asuka Trophy", items_owned_rule([
           "Asuka Trophy",
        ]))
        north_sector_legy_tamers_a_region.locations.extend([
            get_location("Tamer Mitaka", self.player, north_sector_legy_tamers_a_region),
        ])

        amaterasu_tamers_region = Region("Amaterasu Tamers", self.player, self.multiworld)
        amaterasu_region.connect(amaterasu_tamers_region, "Amaterasu + Folder Bag", items_owned_rule(["Folder Bag"]))
        amaterasu_tamers_region.locations.extend([
            get_location("Trooper (Central Park)", self.player, amaterasu_tamers_region),
            get_location("Trooper (West Wire Forest, 1)", self.player, amaterasu_tamers_region),
            get_location("Trooper (West Wire Forest, 2)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Wind Prarie)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Kicking Forest)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Bulk Swamp)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Bulk Bridge)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Tranquil Swamp)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Zhu Que City, 1)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Zhu Que City, 2)", self.player, amaterasu_tamers_region),
            get_location("Trooper (South Badland)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Noise Desert)", self.player, amaterasu_tamers_region),
            get_location("Trooper (North Badland W)", self.player, amaterasu_tamers_region),
            get_location("Trooper (North Badland E)", self.player, amaterasu_tamers_region),
            get_location("Trooper (S Noise Desert)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Boot Mountain, 1)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Boot Mountain, 2)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Snow Mountain, 1)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Snow Mountain, 2)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Freeze Mountain, 1)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Freeze Mountain, 2)", self.player, amaterasu_tamers_region),
            get_location("Trooper (Xuan Wu City)", self.player, amaterasu_tamers_region),
            # other tamers
            get_location("Tamer Takuya", self.player, amaterasu_tamers_region),
            get_location("Tamer Murdock", self.player, amaterasu_tamers_region),
            get_location("Guard Banch", self.player, amaterasu_tamers_region),
            get_location("Tamer Mai", self.player, amaterasu_tamers_region),
            get_location("Tamer Gon", self.player, amaterasu_tamers_region),
        ])

        amaterasu_legy_tamers_region = Region("Amaterasu Legendary Tamers", self.player, self.multiworld)
        amaterasu_tamers_region.connect(amaterasu_legy_tamers_region, "Amaterasu + Folder Bag + Sun Trophy", items_owned_rule(["Sun Trophy"]))
        amaterasu_legy_tamers_region.locations.extend([
            get_location("Tamer Heinrich", self.player, amaterasu_legy_tamers_region),
        ])

        self.multiworld.regions.extend([
            east_sector_tamers_region,
            east_sector_legy_tamers_region,
            south_sector_1_tamers_region,
            south_sector_1_legy_tamers_region,
            south_sector_2_tamers_region,
            west_sector_tamers_region,
            amaterasu_tamers_region,
            amaterasu_legy_tamers_region,
            north_sector_tamers_region,
            north_sector_legy_tamers_a_region,
            north_sector_legy_tamers_s_region
        ])
