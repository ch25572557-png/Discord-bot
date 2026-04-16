import discord
from stock import get_price, reduce_stock
from order import create_order
from points import add_points
from discount import apply
from logs import send_log

class ShopView(discord.ui.View):

    @discord.ui.button(label="Cash", style=discord.ButtonStyle.green)
    async def cash(self, i, b):
        await self.buy(i, "Cash")

    @discord.ui.button(label="Gun", style=discord.ButtonStyle.red)
    async def gun(self, i, b):
        await self.buy(i, "Gun")

    async def buy(self, i, item):

        price = get_price(item)

        if not reduce_stock(item,1):
            return await i.response.send_message("หมด",ephemeral=True)

        total = price

        oid = create_order(i.user.id,item,1,total)

        add_points(i.user.id,1)

        final,d,cost = apply(i.user.id,total)

        await i.response.send_message(
            f"📦 #{oid}\n{item}\n💰 {final}",
            ephemeral=True
        )
