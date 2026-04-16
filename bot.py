import discord
from discord import app_commands
from ticket import TicketView

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ticket")
async def ticket(i: discord.Interaction):

    await i.channel.send("กดสั่งของ", view=TicketView())
    await i.response.send_message("เปิดแล้ว",ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready")

client.run("TOKEN")
