import discord
from discord import app_commands

from ticket import TicketView
from admin import AdminPointsView
from leaderboard import LeaderboardView

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ticket")
async def ticket(interaction):
    await interaction.channel.send(view=TicketView())
    await interaction.response.send_message("OK", ephemeral=True)

@tree.command(name="points")
async def points(interaction):
    await interaction.channel.send(view=AdminPointsView())

@tree.command(name="leaderboard")
async def leaderboard(interaction):
    await interaction.channel.send(view=LeaderboardView())

@client.event
async def on_ready():
    await tree.sync()
    print("READY")

client.run("TOKEN")
