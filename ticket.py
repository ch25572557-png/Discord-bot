import discord
import json
from shop import ShopView
from logs import send_log

config = json.load(open("config.json"))

class TicketView(discord.ui.View):

    @discord.ui.button(label="🛒 สร้าง Ticket", style=discord.ButtonStyle.green)
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        category = discord.utils.get(
            guild.categories,
            id=config["ticket_category_id"]
        )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        view = TicketControlView()

        await channel.send(
            f"🎫 Ticket ของ {interaction.user.mention}",
            view=view
        )

        await interaction.response.send_message(
            f"✅ สร้าง Ticket แล้ว: {channel.mention}",
            ephemeral=True
        )


class TicketControlView(discord.ui.View):

    @discord.ui.button(label="🛒 เปิดร้าน", style=discord.ButtonStyle.green)
    async def shop(self, interaction, button):
        await interaction.channel.send("🛒 ร้านค้า", view=ShopView())
        await interaction.response.send_message("เปิดร้านแล้ว", ephemeral=True)


    @discord.ui.button(label="❌ ปิด Ticket", style=discord.ButtonStyle.red)
    async def close(self, interaction, button):

        await send_log(
            interaction.client,
            f"❌ Ticket ปิดโดย {interaction.user}"
        )

        await interaction.response.send_message("⏳ กำลังปิด Ticket...", ephemeral=True)

        await interaction.channel.delete()
