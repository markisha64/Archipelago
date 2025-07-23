
from typing import Callable
from BaseClasses import CollectionState

def items_owned_rule(items: [str], player: int) -> Callable[[CollectionState, int], bool]:
    return lambda state : state.has_all(items, player)

def items_owned_rule_gen(player: int) -> Callable[Callable[[CollectionState, int], bool]]:
    return lambda items : items_owned_rule(items, player)

