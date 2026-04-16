import discord
from stock import reduce_stock, get_price
from order import create_order
from points import add_points
from discount import apply

class ShopView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.last_order = None

    @discord.ui.button(label="Cash", style=discord.ButtonStyle.green)
    async def cash(self, i, b):
        await self.buy(i,"Cash")

    @discord.ui.button(label="Gun", style=discord.ButtonStyle.red)
    async def gun(self, i, b):
        await self.buy(i,"Gun")

    async def buy(self, i, item):

        if not reduce_stock(item,1):
            return await i.response.send_message("❌ ของหมด", ephemeral=True)

        price = get_price(item)

        oid = create_order(i.user.id,item,1,price)

        self.last_order = oid

        add_points(i.user.id,1)

        final, d = apply(i.user.id,price)

        await i.response.send_message(
            f"📦 Order #{oid}\n💰 {final}",
            ephemeral=True
        )
