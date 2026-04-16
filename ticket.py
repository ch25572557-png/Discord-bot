import discord
import asyncio
import json

from shop import ShopView
from order import load, update_status
from order_channel import get_order_channel

config = json.load(open("config.json"))

active = {}

class TicketView(discord.ui.View):

    @discord.ui.button(label="🎫 Ticket", style=discord.ButtonStyle.green)
    async def create(self, interaction, button):

        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(
            guild.categories,
            id=config["ticket_category_id"]
        )

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

        active[interaction.channel.id] = asyncio.get_event_loop().time()

        await interaction.channel.send(view=ShopView())


    @discord.ui.button(label="📦 Send", style=discord.ButtonStyle.blurple)
    async def send(self, interaction, button):

        db = load()
        oid = str(db["counter"])

        update_status(oid, "sent")

        ch = await get_order_channel(interaction.guild, oid)

        await ch.send(f"📦 Order #{oid} sent")

        await interaction.channel.delete()


async def auto_close(channel):

    while True:
        await asyncio.sleep(60)

        now = asyncio.get_event_loop().time()
        last = active.get(channel.id,0)

        if now - last > config["auto_close_minutes"] * 60:
            try:
                await channel.delete()
            except:
                pass
            break
