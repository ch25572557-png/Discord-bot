import discord
import os
from discord import app_commands

from ticket import TicketView
from shop import ShopView
from admin import AdminStockView, AdminPointsView

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print("READY:", client.user)

@tree.command(name="ticket")
async def ticket(interaction):
    await interaction.response.send_message("🎫 Ticket", view=TicketView())

@tree.command(name="admin")
async def admin(interaction):
    await interaction.response.send_message("👑 Admin", view=AdminStockView())

@tree.command(name="points")
async def points(interaction):
    await interaction.response.send_message("💰 Points", view=AdminPointsView())

client.run(os.getenv("TOKEN"))
