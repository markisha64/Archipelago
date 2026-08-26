
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
    BATTLED_TAMERS = 4
    AUCTION = 5
    UNK6 = 6
    BOSSES = 7

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

ITEM_BOX_LOCATIONS: Dict[str, DMW2003Flag] = {f"Item Box \"{entry['server']} {entry['name']} #{entry['i']}\"": DMW2003Flag(entry["flag"], DMW2003FlagType.ITEM_BOX)  for entry in item_boxes_json}

STORY_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Beat Keith": DMW2003Flag(22, DMW2003FlagType.STORY),
    "Beat Game Master": DMW2003Flag(80, DMW2003FlagType.STORY),
    "Beat Magami President": DMW2003Flag(95, DMW2003FlagType.STORY),
    "Beat Qing Long Chief": DMW2003Flag(167, DMW2003FlagType.STORY),
    "Beat Ice Witch": DMW2003Flag(25, DMW2003FlagType.STORY),
    "Beat Fire Knight": DMW2003Flag(64, DMW2003FlagType.STORY),
    "Beat Dark Knight": DMW2003Flag(66, DMW2003FlagType.STORY),
    "Beat Ice Master": DMW2003Flag(131, DMW2003FlagType.STORY),
    "Beat Fire Master": DMW2003Flag(133, DMW2003FlagType.STORY),
    "Beat Dark Master": DMW2003Flag(135, DMW2003FlagType.STORY),
}

BOSSES_LOCATIONS: Dict[str,DMW2003Flag] = {
    "Beat Pharaohmon": DMW2003Flag(0, DMW2003FlagType.BOSSES),
    "Beat Master Tyrannomon": DMW2003Flag(1, DMW2003FlagType.BOSSES),
    "Beat Zanbamon": DMW2003Flag(2, DMW2003FlagType.BOSSES),
    "Beat Datamon": DMW2003Flag(3, DMW2003FlagType.BOSSES),
    "Beat HiAndromon": DMW2003Flag(4, DMW2003FlagType.BOSSES),
    "Beat BK MegaGargomon": DMW2003Flag(7, DMW2003FlagType.BOSSES),
    "Beat BK Imperialdramon": DMW2003Flag(9, DMW2003FlagType.BOSSES),
    "Beat BK Seraphimon": DMW2003Flag(10, DMW2003FlagType.BOSSES),
    "Beat BK WarGrowlmon": DMW2003Flag(11, DMW2003FlagType.BOSSES),
    "Beat BK KingNumemon": DMW2003Flag(12, DMW2003FlagType.BOSSES),
}

NPC2_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Hidden Bits": DMW2003Flag(52, DMW2003FlagType.NPC2),
    "Beat MetalGreymon": DMW2003Flag(18, DMW2003FlagType.NPC2),
    "Beat Armormon": DMW2003Flag(23, DMW2003FlagType.NPC2),
    "Beat Paildramon": DMW2003Flag(25, DMW2003FlagType.NPC2),
    "Beat WarGrowlmon": DMW2003Flag(19, DMW2003FlagType.NPC2),
    "Beat MagnaAngemon": DMW2003Flag(20, DMW2003FlagType.NPC2),
    "Beat Taomon": DMW2003Flag(21, DMW2003FlagType.NPC2),
    "Beat Kyukimon": DMW2003Flag(22, DMW2003FlagType.NPC2),
    "Beat GrapLeomon": DMW2003Flag(24, DMW2003FlagType.NPC2),
}

QUEST_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Beat Seiryu Leader": DMW2003Flag(5, DMW2003FlagType.QUEST),
    "Beat Suzaku Leader": DMW2003Flag(11, DMW2003FlagType.QUEST),
    "DE Sincerity": DMW2003Flag(15, DMW2003FlagType.QUEST),
    "Beat Fake Byakko Leader": DMW2003Flag(16, DMW2003FlagType.QUEST),
    "Beat Byakko Leader": DMW2003Flag(17, DMW2003FlagType.QUEST),
    "Beat WaruMonzaemon": DMW2003Flag(19, DMW2003FlagType.QUEST),
    "Beat A.o.A Ambusher": DMW2003Flag(20, DMW2003FlagType.QUEST),
    "Beat Bulbmon": DMW2003Flag(27, DMW2003FlagType.QUEST),
    "Beat Zhu Que Chief": DMW2003Flag(29, DMW2003FlagType.QUEST),
    "DE Knowledge": DMW2003Flag(30, DMW2003FlagType.QUEST),
    "Beat Genbu Leader": DMW2003Flag(31, DMW2003FlagType.QUEST),
    "Beat Bai Hu Chief": DMW2003Flag(35, DMW2003FlagType.QUEST),
    "Beat Xuan Wu Chief": DMW2003Flag(36, DMW2003FlagType.QUEST),
    "Beat Galacticmon": DMW2003Flag(45, DMW2003FlagType.QUEST)
}

BATTLED_TAMERS_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Tamer Genji": DMW2003Flag(0, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Natsumi": DMW2003Flag(1, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Mitch": DMW2003Flag(2, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Catherine": DMW2003Flag(3, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Lucia": DMW2003Flag(4, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Robert": DMW2003Flag(5, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Akiba": DMW2003Flag(6, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Bob": DMW2003Flag(7, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Tomomi": DMW2003Flag(8, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Chris": DMW2003Flag(9, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Andy": DMW2003Flag(10, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer George": DMW2003Flag(11, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Mei Lin": DMW2003Flag(12, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Jessica": DMW2003Flag(13, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Gordon": DMW2003Flag(14, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Alice": DMW2003Flag(15, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Nakano": DMW2003Flag(16, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Haruka": DMW2003Flag(17, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Poemy": DMW2003Flag(18, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Shingo": DMW2003Flag(19, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Makoto": DMW2003Flag(20, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Brown": DMW2003Flag(21, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Pierre": DMW2003Flag(22, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Mitaka": DMW2003Flag(23, DMW2003FlagType.BATTLED_TAMERS),
    # Troopers
    "Trooper (Central Park)": DMW2003Flag(27, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (West Wire Forest, 1)": DMW2003Flag(28, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (West Wire Forest, 2)": DMW2003Flag(29, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Wind Prarie)": DMW2003Flag(30, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Kicking Forest)": DMW2003Flag(31, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Bulk Swamp)": DMW2003Flag(32, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Bulk Bridge)": DMW2003Flag(33, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Tranquil Swamp)": DMW2003Flag(34, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Zhu Que City, 1)": DMW2003Flag(35, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Zhu Que City, 2)": DMW2003Flag(36, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (South Badland)": DMW2003Flag(37, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Noise Desert)": DMW2003Flag(38, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (North Badland W)": DMW2003Flag(39, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (North Badland E)": DMW2003Flag(40, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (S Noise Desert)": DMW2003Flag(41, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Boot Mountain, 1)": DMW2003Flag(46, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Boot Mountain, 2)": DMW2003Flag(47, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Snow Mountain, 1)": DMW2003Flag(48, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Snow Mountain, 2)": DMW2003Flag(49, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Freeze Mountain, 1)": DMW2003Flag(50, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Freeze Mountain, 2)": DMW2003Flag(51, DMW2003FlagType.BATTLED_TAMERS),
    "Trooper (Xuan Wu City)": DMW2003Flag(58, DMW2003FlagType.BATTLED_TAMERS),
    # Other Amaterasu Tamers
    "Tamer Heinrich": DMW2003Flag(42, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Takuya": DMW2003Flag(43, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Murdock": DMW2003Flag(44, DMW2003FlagType.BATTLED_TAMERS),
    "Guard Banch": DMW2003Flag(45, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Mai": DMW2003Flag(52, DMW2003FlagType.BATTLED_TAMERS),
    "Tamer Gon": DMW2003Flag(53, DMW2003FlagType.BATTLED_TAMERS),
}

UNK6_LOCATIONS: Dict[str, DMW2003Flag] = {
    "Zhu Que Leader": DMW2003Flag(14, DMW2003FlagType.UNK6),
    "Bai Hu Leader": DMW2003Flag(15, DMW2003FlagType.UNK6),
    "Qing Long Leader": DMW2003Flag(16, DMW2003FlagType.UNK6),
    "Xuan Wu Leader": DMW2003Flag(17, DMW2003FlagType.UNK6)
} 

AUCTION_LOCATIONS: Dict[str, DMW2003Flag] = {f"Auction #{i}": DMW2003Flag(i, DMW2003FlagType.AUCTION) for i in range(16)}

ALL_LOCATIONS_TABLE: Dict[str, DMW2003Flag] ={} 
ALL_LOCATIONS_TABLE.update(ITEM_BOX_LOCATIONS)
ALL_LOCATIONS_TABLE.update(STORY_LOCATIONS)
ALL_LOCATIONS_TABLE.update(BOSSES_LOCATIONS)
ALL_LOCATIONS_TABLE.update(NPC2_LOCATIONS)
ALL_LOCATIONS_TABLE.update(QUEST_LOCATIONS)
ALL_LOCATIONS_TABLE.update(BATTLED_TAMERS_LOCATIONS)
ALL_LOCATIONS_TABLE.update(AUCTION_LOCATIONS)
ALL_LOCATIONS_TABLE.update(UNK6_LOCATIONS)

ALL_LOCATIONS_BY_KEY: Dict[int, DMW2003Flag] = {entry.to_key(): entry for (name, entry) in ALL_LOCATIONS_TABLE.items()}

# Trooper Mirrors
ALL_LOCATIONS_BY_KEY[DMW2003Flag(60, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(27, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(63, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(30, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(64, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(31, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(65, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(32, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(66, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(33, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(67, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(34, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(70, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(37, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(72, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(38, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(71, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(39, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(73, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(40, DMW2003FlagType.BATTLED_TAMERS)
ALL_LOCATIONS_BY_KEY[DMW2003Flag(74, DMW2003FlagType.BATTLED_TAMERS).to_key()] = DMW2003Flag(41, DMW2003FlagType.BATTLED_TAMERS)

def get_location(name: str, player: int, parent: Region) -> DMW2003Location:
    location = ALL_LOCATIONS_TABLE[name]
    
    return DMW2003Location(player, name, location.to_key(), parent)

def get_beat_galacticmon(player: int, parent: Region) -> DMW2003Location:
    return DMW2003Location(player, "Beat Galacticmon", None, parent)
