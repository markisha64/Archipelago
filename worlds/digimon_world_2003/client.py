from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .locations import ALL_LOCATIONS_BY_ID

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

INVENTORY_OFFSET = 0x48db0

class DMW2003Client(BizHawkClient):
    game = "Digimon World 2003"
    system = "PSX"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x100fc, 20, "MainRAM")]))[0]).decode("ascii")
            if rom_name != "BESLES-03936DMW3-EUR":
                return False
        except bizhawk.RequestFailedError:
            return False 

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        self.last_timestamp = 0
        self.expected_inventory = [0 for _ in range(403)]

        return True

    def get_timestamp(self, clock_bytes) -> int:
        hours = int.from_bytes(clock_bytes[0:2], "little")
        minutes = int.from_bytes(clock_bytes[2:4], "little")
        seconds = int.from_bytes(clock_bytes[4:6], "little")

        return hours * 3600 + minutes * 60 + seconds

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            clock_bytes, inventory, quest_bytes, stage_id_bytes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x48d80, 6, "MainRAM"),
                    (INVENTORY_OFFSET, 403, "MainRAM"),
                    # TODO: replace with proper addresses
                    (0x48d80, 4, "MainRAM"),
                    (0x48d80, 4, "MainRAM"),
                ]
            )
            timestamp = self.get_timestamp(clock_bytes)

            quest = int.from_bytes(quest_bytes, "little")
            stage_id = int.from_bytes(stage_id_bytes, "little")
            
            # TODO: replace with stage_id e value with proper value
            if not ctx.finished_game and quest == 45 and stage_id >> 7 == 5:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            update_list = {}
            checked_locations = []
            
            # TODO: make some kind of check whether were in main menu
            # cause it can be dangerous to override expected_inventory with empty inventory
            # and then load a timestamp and move it forwards

            if timestamp <= self.last_timestamp: 
                # loaded older save
                self.expected_inventory = [x for x in inventory]
            else:
                # check whether you gained new items
                self.last_timestamp = timestamp

                for i in range(2, 403):
                    if inventory[i] > self.expected_inventory[i]:
                        # TODO: i need to also unequip items here 
                        update_list[i] = self.expected_inventory[i]

                        # check if item in pool
                        if i in ALL_LOCATIONS_BY_ID:
                            j = inventory[i] - self.expected_inventory[i]

                            checked_locations.extend([i for _ in range(j)])
                    else:
                        self.expected_inventory[i] = inventory[i]

            self.last_timestamp = timestamp
            last_awarded_item_index = int.from_bytes(inventory[0:2], "little")
            item_count = len(ctx.items_received)

            if last_awarded_item_index < item_count:
                for item in ctx.items_received[last_awarded_item_index:]:
                    i = item.item
                    self.expected_inventory[i] = min(99, self.expected_inventory[i] + 1)
                    update_list[i] = self.expected_inventory[i]

            # locations
            if checked_locations:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": checked_locations 
                }])

            # update inventory
            writes = [(
                INVENTORY_OFFSET + i,
                v.to_bytes(1, "little"),
                "MainRAM"
            ) for i, v in update_list.items()]            

            # update last awarded index
            if last_awarded_item_index < item_count:
                writes.append((
                    INVENTORY_OFFSET,
                    item_count.to_bytes(2, "little"),
                    "MainRAM"
                ))

            if writes:
                await bizhawk.write(ctx.bizhawk_ctx, writes)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
