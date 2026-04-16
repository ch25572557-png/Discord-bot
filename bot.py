import discord
from discord import app_commands
from discord.ui import View, Button
import os
import json

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ---------------- STOCK SYSTEM ----------------

def load_stock():
    try:
        with open("stock.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_stock(data):
    with open("stock.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------------- ORDER STATUS VIEW ----------------

class StatusView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def update_embed(self, interaction: discord.Interaction, status: str, color: discord.Color):
        embed = interaction.message.embeds[0]

        # field สถานะอยู่ตำแหน่ง 3
        embed.set_field_at(3, name="📌 สถานะ", value=status, inline=False)

        embed.color = color

        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()

    @discord.ui.button(label="📦 เตรียมสินค้า", style=discord.ButtonStyle.primary)
    async def preparing(self, interaction: discord.Interaction, button: Button):
        await self.update_embed(
            interaction,
            "📦 กำลังเตรียมสินค้า",
            discord.Color.blue()
        )

    @discord.ui.button(label="🚚 กำลังส่ง", style=discord.ButtonStyle.secondary)
    async def shipping(self, interaction: discord.Interaction, button: Button):
        await self.update_embed(
            interaction,
            "🚚 กำลังส่งสินค้า",
            discord.Color.orange()
        )

    @discord.ui.button(label="🟢 ส่งแล้ว", style=discord.ButtonStyle.success)
    async def done(self, interaction: discord.Interaction, button: Button):
        await self.update_embed(
            interaction,
            "🟢 ส่งสินค้าแล้ว",
            discord.Color.green()
        )

# ---------------- SEND ORDER ----------------

@tree.command(name="ส่งของ", description="สร้างออเดอร์สินค้า")
@app_commands.describe(
    ลูกค้า="ผู้รับ",
    สินค้า="ชื่อสินค้า",
    จำนวน="จำนวน"
)
async def ส่งของ(interaction: discord.Interaction, ลูกค้า: discord.User, สินค้า: str, จำนวน: str):

    embed = discord.Embed(
        title="🛍️ ORDER SYSTEM",
        color=discord.Color.yellow()
    )

    embed.add_field(name="👤 ผู้รับ", value=ลูกค้า.mention, inline=False)
    embed.add_field(name="📦 สินค้า", value=สินค้า, inline=False)
    embed.add_field(name="🔢 จำนวน", value=จำนวน, inline=False)
    embed.add_field(name="📌 สถานะ", value="🟡 รอดำเนินการ", inline=False)

    await interaction.response.send_message("✅ สร้างออเดอร์แล้ว!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StatusView())

# ---------------- STOCK COMMANDS ----------------

@tree.command(name="เพิ่มสต็อก", description="เพิ่มสินค้าเข้า stock")
async def add_stock(interaction: discord.Interaction, สินค้า: str, จำนวน: int):

    data = load_stock()

    if สินค้า in data:
        data[สินค้า] += จำนวน
    else:
        data[สินค้า] = จำนวน

    save_stock(data)

    await interaction.response.send_message(f"✅ เพิ่ม {สินค้า} +{จำนวน}")

@tree.command(name="ลดสต็อก", description="ลดสินค้าออกจาก stock")
async def remove_stock(interaction: discord.Interaction, สินค้า: str, จำนวน: int):

    data = load_stock()

    if สินค้า not in data:
        await interaction.response.send_message("❌ ไม่มีสินค้านี้")
        return

    data[สินค้า] -= จำนวน

    if data[สินค้า] <= 0:
        del data[สินค้า]

    save_stock(data)

    await interaction.response.send_message(f"🗑️ ลด {สินค้า} -{จำนวน}")

@tree.command(name="ดูสต็อก", description="ดูสินค้าทั้งหมด")
async def show_stock(interaction: discord.Interaction):

    data = load_stock()

    if not data:
        await interaction.response.send_message("📦 ยังไม่มีสินค้า")
        return

    msg = "**📦 STOCK:**\n"
    for item, qty in data.items():
        msg += f"- {item}: {qty}\n"

    await interaction.response.send_message(msg)

# ---------------- READY ----------------

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)
