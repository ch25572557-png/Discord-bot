import discord
import os
from discord import app_commands

from ticket import TicketView
from admin import AdminStockView, AdminPointsView
from leaderboard import LeaderboardView

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# --------------------
# SLASH COMMANDS
# --------------------

@tree.command(name="ticket")
async def ticket(interaction: discord.Interaction):
    await interaction.channel.send(view=TicketView())
    await interaction.response.send_message("OK", ephemeral=True)


@tree.command(name="stock")
async def stock(interaction: discord.Interaction):
    await interaction.channel.send(view=AdminStockView())


@tree.command(name="points")
async def points(interaction: discord.Interaction):
    await interaction.channel.send(view=AdminPointsView())


@tree.command(name="leaderboard")
async def lb(interaction: discord.Interaction):
    await interaction.channel.send(view=LeaderboardView())


# --------------------
# READY EVENT
# --------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"READY: {client.user}")


# --------------------
# RUN BOT (IMPORTANT FIX)
# --------------------
client.run(os.getenv("TOKEN"))
