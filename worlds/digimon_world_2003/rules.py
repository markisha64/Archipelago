
from typing import Callable
from BaseClasses import CollectionState

def items_owned_rule(items: [str]) -> Callable[[CollectionState], bool]:
    return lambda state : state.has_all(items)
