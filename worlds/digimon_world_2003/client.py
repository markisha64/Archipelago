from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .locations import check_flag, DMW2003Flag, DMW2003FlagType

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

CLOCK_OFFSET = 0x48d80
INVENTORY_OFFSET = 0x48db0
QUEST_OFFSET = 0x4b370
STAGE_ID_OFFSET = 0x4b3f8
ITEM_BOXES = 0x4b378


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
        self.item_boxes = [False for _ in range(8 * 18)]

        return True

    def get_timestamp(self, clock_bytes) -> int:
        hours = int.from_bytes(clock_bytes[0:2], "little")
        minutes = int.from_bytes(clock_bytes[2:4], "little")
        seconds = int.from_bytes(clock_bytes[4:6], "little")

        return hours * 3600 + minutes * 60 + seconds

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            clock_bytes, inventory, quest_bytes, stage_id_bytes, item_boxes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (CLOCK_OFFSET, 6, "MainRAM"),
                    (INVENTORY_OFFSET, 403, "MainRAM"),
                    (QUEST_OFFSET, 4, "MainRAM"),
                    (STAGE_ID_OFFSET, 4, "MainRAM"),
                    (ITEM_BOXES, 18, "MainRAM"),
                ]
            )
            # timestamp = self.get_timestamp(clock_bytes)

            quest = int.from_bytes(quest_bytes, "little")
            stage_id = int.from_bytes(stage_id_bytes, "little")

            group_id = stage_id >> 8

            # skip doing anything if we on main menu / load menu / country select
            if group_id == 22 or group_id == 14 or group_id == 12:
                return

            if not ctx.finished_game and quest == 45 and group_id == 2:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            update_list = {}
            checked_locations = []

            # item boxes
            for i in range(18 * 8):
                if check_flag(item_boxes, i) and not self.item_boxes[i]:
                    self.item_boxes[i] = True
                    checked_locations.append(DMW2003Flag(i, DMW2003FlagType.ITEM_BOX).to_key())

            # self.last_timestamp = timestamp
            last_awarded_item_index = int.from_bytes(inventory[0:2], "little")
            item_count = len(ctx.items_received)

            # print(f"timestamp: {timestamp}")
            # print(f"last_awarded_item_index: {last_awarded_item_index}")
            # print(f"item_count: {item_count}")

            if last_awarded_item_index < item_count:
                for item in ctx.items_received[last_awarded_item_index:]:
                    update_list[item.item] = inventory[item.item] + 1

            # # locations
            if checked_locations:
                print(checked_locations)
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
