import discord
import asyncio
import json

config = json.load(open("config.json"))
active = {}

class TicketView(discord.ui.View):

    @discord.ui.button(label="🎫 เปิด Ticket", style=discord.ButtonStyle.green)
    async def open(self, interaction, button):

        guild = interaction.guild
        user = interaction.user

        category = guild.get_channel(config["ticket_category_id"])

        if category is None:
            category = discord.utils.get(guild.categories, id=config["ticket_category_id"])

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category
        )

        await channel.set_permissions(user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)

        await channel.send(f"🎫 {user.mention}", view=TicketControl())

        active[channel.id] = asyncio.get_event_loop().time()

        await interaction.response.send_message(f"✅ {channel.mention}", ephemeral=True)

        interaction.client.loop.create_task(auto_close(channel))


class TicketControl(discord.ui.View):

    @discord.ui.button(label="🛒 Shop", style=discord.ButtonStyle.green)
    async def shop(self, interaction, button):
        from shop import ShopView
        await interaction.channel.send(view=ShopView())


async def auto_close(channel):

    while True:
        await asyncio.sleep(60)

        now = asyncio.get_event_loop().time()
        last = active.get(channel.id, 0)

        if now - last > config["auto_close_minutes"] * 60:
            await channel.delete()
            break
