import discord

from stock import reduce_stock, get_price
from order import create_order
from points import add_points
from discount import get_discount
from order_channel import get_order_channel

class ShopView(discord.ui.View):

    @discord.ui.button(label="🛒 Buy", style=discord.ButtonStyle.green)
    async def buy(self, interaction: discord.Interaction, button):

        user_id = interaction.user.id
        item = "cash"

        price = get_price(item)
        discount = get_discount(user_id)

        final_price = price - (price * discount)

        if not reduce_stock(item, 1):
            return await interaction.response.send_message("❌ ของหมด", ephemeral=True)

        order_id = create_order(user_id, item, 1, final_price)

        add_points(user_id, 1)

        channel = await get_order_channel(interaction.guild, order_id)

        if channel:
            await channel.send(f"🆕 Order #{order_id}\n💰 {final_price}")

        await interaction.response.send_message(f"✅ Order #{order_id}", ephemeral=True)
