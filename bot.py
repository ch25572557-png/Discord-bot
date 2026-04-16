import discord
from discord import app_commands
from discord.ui import View, Button
import os
import json
import random
import datetime

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ---------------- LOG CHANNEL ----------------
LOG_CHANNEL_ID = 1494258803422662856

async def send_log(message: str):
    channel = client.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)

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

# ---------------- ORDERS ----------------

def load_orders():
    try:
        with open("orders.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_orders(data):
    with open("orders.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------------- STATUS BUTTON VIEW ----------------

class StatusView(View):
    def __init__(self, order_id: str):
        super().__init__(timeout=None)
        self.order_id = order_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ เฉพาะแอดมินเท่านั้น", ephemeral=True)
            return False
        return True

    async def update_status(self, interaction: discord.Interaction, status: str, color: discord.Color):

        orders = load_orders()
        order = orders.get(self.order_id)

        if not order:
            await interaction.response.send_message("❌ ไม่พบออเดอร์", ephemeral=True)
            return

        # update data
        order["status"] = status
        orders[self.order_id] = order
        save_orders(orders)

        # update embed
        embed = interaction.message.embeds[0]
        embed.set_field_at(3, name="📌 สถานะ", value=status, inline=False)
        embed.color = color

        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()

        # 🔔 DM ลูกค้า
        try:
            user = await client.fetch_user(order["user_id"])
            await user.send(
                f"📦 ออเดอร์ #{self.order_id}\n🔄 สถานะอัปเดต: {status}"
            )
        except:
            pass

        # 📜 LOG
        await send_log(
            f"📢 ORDER UPDATE\n"
            f"👤 Admin: {interaction.user} ({interaction.user.id})\n"
            f"🧾 Order: #{self.order_id}\n"
            f"🔄 Status: {status}\n"
            f"⏰ {datetime.datetime.now()}"
        )

    @discord.ui.button(label="📦 เตรียมสินค้า", style=discord.ButtonStyle.primary)
    async def preparing(self, interaction: discord.Interaction, button: Button):
        await self.update_status(interaction, "📦 กำลังเตรียมสินค้า", discord.Color.blue())

    @discord.ui.button(label="🚚 กำลังส่ง", style=discord.ButtonStyle.secondary)
    async def shipping(self, interaction: discord.Interaction, button: Button):
        await self.update_status(interaction, "🚚 กำลังส่งสินค้า", discord.Color.orange())

    @discord.ui.button(label="🟢 ส่งแล้ว", style=discord.ButtonStyle.success)
    async def done(self, interaction: discord.Interaction, button: Button):
        await self.update_status(interaction, "🟢 ส่งสินค้าแล้ว", discord.Color.green())

# ---------------- CREATE ORDER ----------------

@tree.command(name="ส่งของ", description="สร้างออเดอร์สินค้า")
async def ส่งของ(interaction: discord.Interaction, ลูกค้า: discord.User, สินค้า: str, จำนวน: str):

    order_id = str(random.randint(1000, 9999))

    orders = load_orders()
    orders[order_id] = {
        "user_id": ลูกค้า.id,
        "สินค้า": สินค้า,
        "จำนวน": จำนวน,
        "status": "🟡 รอดำเนินการ"
    }
    save_orders(orders)

    embed = discord.Embed(
        title=f"🛍️ ORDER #{order_id}",
        color=discord.Color.yellow()
    )

    embed.add_field(name="👤 ผู้รับ", value=ลูกค้า.mention, inline=False)
    embed.add_field(name="📦 สินค้า", value=สินค้า, inline=False)
    embed.add_field(name="🔢 จำนวน", value=จำนวน, inline=False)
    embed.add_field(name="📌 สถานะ", value="🟡 รอดำเนินการ", inline=False)

    await interaction.response.send_message("✅ สร้างออเดอร์แล้ว!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=StatusView(order_id))

    await send_log(
        f"🛍️ NEW ORDER #{order_id}\n"
        f"👤 User: {ลูกค้า} ({ลูกค้า.id})\n"
        f"📦 {สินค้า} x{จำนวน}\n"
        f"⏰ {datetime.datetime.now()}"
    )

# ---------------- STOCK ----------------

@tree.command(name="เพิ่มสต็อก")
async def add_stock(interaction: discord.Interaction, สินค้า: str, จำนวน: int):
    data = load_stock()
    data[สินค้า] = data.get(สินค้า, 0) + จำนวน
    save_stock(data)

    await interaction.response.send_message(f"✅ เพิ่ม {สินค้า} +{จำนวน}")

@tree.command(name="ลดสต็อก")
async def remove_stock(interaction: discord.Interaction, สินค้า: str, จำนวน: int):
    data = load_stock()
    if สินค้า not in data:
        return await interaction.response.send_message("❌ ไม่มีสินค้า")

    data[สินค้า] -= จำนวน
    if data[สินค้า] <= 0:
        del data[สินค้า]

    save_stock(data)
    await interaction.response.send_message(f"🗑️ ลด {สินค้า} -{จำนวน}")

@tree.command(name="ดูสต็อก")
async def show_stock(interaction: discord.Interaction):
    data = load_stock()
    if not data:
        return await interaction.response.send_message("📦 ไม่มีสินค้า")

    msg = "**📦 STOCK:**\n"
    for k, v in data.items():
        msg += f"- {k}: {v}\n"

    await interaction.response.send_message(msg)

# ---------------- READY ----------------

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run(TOKEN)
