import discord

from stock import reduce_stock, get_price
from order import create_order
from points import add_points
from discount import get_discount
from order_channel import get_order_channel

class ShopView(discord.ui.View):

    @discord.ui.button(label="🛒 Buy", style=discord.ButtonStyle.green)
    async def buy(self, interaction, button):

        item = "cash"

        price = get_price(item)
        discount = get_discount(interaction.user.id)

        final_price = price - (price * discount)

        if not reduce_stock(item, 1):
            return await interaction.response.send_message("❌ ของหมด", ephemeral=True)

        oid = create_order(interaction.user.id, item, 1, final_price)

        add_points(interaction.user.id, 1)

        ch = await get_order_channel(interaction.guild, oid)

        await ch.send(f"🆕 Order #{oid}\n💰 {final_price}")

        await interaction.response.send_message(f"Order #{oid} created", ephemeral=True)
