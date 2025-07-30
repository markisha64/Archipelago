
from dataclasses import dataclass

from Options import OptionDict, PerGameCommonOptions

class Shops(OptionDict):
    display_name = "shops"

class ItemBoxes(OptionDict):
    display_name = "item_boxes"

@dataclass
class DMW2003Options(PerGameCommonOptions):
    shops: Shops
    item_boxes: ItemBoxes
