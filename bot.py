import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ส่งของ", description="แจ้งส่งของสำเร็จ")
@app_commands.describe(
    ลูกค้า="ผู้รับ",
    สินค้า="ชื่อสินค้า",
    จำนวน="จำนวน"
)
async def ส่งของ(interaction: discord.Interaction, ลูกค้า: discord.User, สินค้า: str, จำนวน: str):

    embed = discord.Embed(
        title="🛍️ ORDER SUCCESS",
        color=discord.Color.green()
    )

    embed.add_field(name="👤 ผู้รับ", value=ลูกค้า.mention, inline=False)
    embed.add_field(name="📦 สินค้า", value=สินค้า, inline=False)
    embed.add_field(name="🔢 จำนวน", value=จำนวน, inline=False)
    embed.add_field(name="📌 สถานะ", value="🟢 ส่งสินค้าเรียบร้อย", inline=False)

    await interaction.response.send_message("✅ ส่งของเรียบร้อยแล้ว!", ephemeral=True)
    await interaction.channel.send(embed=embed)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)
