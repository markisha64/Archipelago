
from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice

class FillerItemPool(Choice):
    """Filler items to be added to the Pool."""
    display_name = "Filler Item Pool"
    option_buyable = 0
    option_sellable = 1
    default = 0

@dataclass
class DMW2003Options(PerGameCommonOptions):
    filler_item_pool: FillerItemPool
