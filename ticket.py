import discord
from shop import ShopView

class TicketView(discord.ui.View):

    @discord.ui.button(label="🛒 สั่งของ", style=discord.ButtonStyle.green)
    async def buy(self, i, b):

        await i.channel.send("🛒 ร้าน", view=ShopView())
        await i.response.send_message("เปิดร้านแล้ว",ephemeral=True)
