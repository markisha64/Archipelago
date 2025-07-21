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
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x100, 6, "ROM")]))[0]).decode("ascii")
            if rom_name != "SLES_039.36":
                return False
        except bizhawk.RequestFailedError:
            return False 

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            inventory = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x80048db0, 403, "ram")]
            ))[0]

            print(inventory)


        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
