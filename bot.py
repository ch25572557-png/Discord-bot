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

@client.event
async def on_ready():
    await tree.sync()
    print(f"READY: {client.user}")

@tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="stock")
async def stock(interaction):
    await interaction.channel.send(view=AdminStockView())

@tree.command(name="points")
async def points(interaction):
    await interaction.channel.send(view=AdminPointsView())

@tree.command(name="leaderboard")
async def leaderboard(interaction):
    await interaction.channel.send(view=LeaderboardView())

token = os.getenv("TOKEN")

if not token:
    print("❌ TOKEN missing")
else:
    client.run(token)
