import discord
import asyncio
import json

from shop import ShopView

config = json.load(open("config.json"))
active = {}

class TicketView(discord.ui.View):

    @discord.ui.button(label="🎫 Ticket", style=discord.ButtonStyle.green)
    async def create(self, interaction, button):

        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, id=config["ticket_category_id"])

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category
        )

        active[channel.id] = asyncio.get_event_loop().time()

        await channel.send("🎫 Ticket Open", view=TicketControl())
        interaction.client.loop.create_task(auto_close(channel))

        await interaction.response.send_message(channel.mention, ephemeral=True)


class TicketControl(discord.ui.View):

    @discord.ui.button(label="🛒 Shop", style=discord.ButtonStyle.green)
    async def shop(self, interaction, button):
        await interaction.channel.send(view=ShopView())


async def auto_close(channel):

    while True:
        await asyncio.sleep(60)

        now = asyncio.get_event_loop().time()
        last = active.get(channel.id, 0)

        if now - last > config["auto_close_minutes"] * 60:
            try:
                await channel.delete()
            except:
                pass
            break
