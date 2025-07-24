from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


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
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        self.last_timestamp = 0
        self.expected_inventory = [0 for _ in range(403)]

        return True

    async def get_timestamp(self, ctx: "BizHawkClientContext") -> int:
        clock_bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x48d80, 6, "MainRAM")]
        ))

        hours = int.from_bytes(clock_bytes[0:2], "little")
        minutes = int.from_bytes(clock_bytes[2:4], "little")
        seconds = int.from_bytes(clock_bytes[4:6], "little")

        return hours * 3600 + minutes * 60 + seconds

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            timestamp = await self.get_timestamp(ctx)
            
            inventory = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x48db0, 403, "MainRAM")]
            ))

            if timestamp <= self.last_timestamp: 
                # reloaded save?
                pass
            else:
                # check whether you gained new items
                self.last_timestamp = timestamp

                to_remove = []

                for i in range(2, 403):
                    if inventory[i] > self.expected_inventory[i]:
                        to_remove.append((i, self.expected_inventory[i]))
                    else:
                        self.expected_inventory[i] = inventory[i]
                
                pass
            
            print(inventory)


        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
