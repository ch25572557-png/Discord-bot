import discord
from discord import app_commands
import json
import os
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ================= CONFIG =================
TICKET_CATEGORY_NAME = "📩 Ticket"
ORDER_CATEGORY_NAME = "🧾 Orders"
LOG_CHANNEL_ID = 1494258803422662856
VIP_ROLE_ID = 0  # ใส่ VIP Role ID

tickets = {}

# ================= DB =================
def load(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ================= UTIL =================
def get_category(guild, name):
    return discord.utils.get(guild.categories, name=name)

async def log(msg):
    ch = client.get_channel(LOG_CHANNEL_ID)
    if ch:
        await ch.send(msg)

# ================= VIP =================
async def check_vip_warning(member, points):
    if points == 40:
        try:
            await member.send("⚠️ อีก 10 แต้มจะได้ VIP 🎉")
        except:
            pass

async def update_vip(member, points):

    role = member.guild.get_role(VIP_ROLE_ID)
    if not role:
        return

    if points >= 50:
        if role not in member.roles:
            await member.add_roles(role)
    else:
        if role in member.roles:
            await member.remove_roles(role)

    if points < 50:
        await check_vip_warning(member, points)

# ================= TICKET =================
class TicketView(discord.ui.View):

    @discord.ui.button(label="🎫 เปิด Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        category = get_category(guild, TICKET_CATEGORY_NAME)

        if category is None:
            return await interaction.response.send_message("❌ ไม่มีหมวด Ticket", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        tickets[channel.id] = interaction.user.id

        await interaction.response.send_message(f"🎫 เปิด Ticket แล้ว {channel.mention}", ephemeral=True)

# ================= ORDER =================
def get_ticket_user(channel_id):
    return tickets.get(channel_id)

@tree.command(name="ส่งของ")
async def send_order(interaction: discord.Interaction, สินค้า: str, จำนวน: str, ราคา: int):

    user_id = get_ticket_user(interaction.channel.id)
    if not user_id:
        return await interaction.response.send_message("❌ ใช้ได้เฉพาะ Ticket", ephemeral=True)

    guild = interaction.guild
    member = guild.get_member(user_id)
    user = await client.fetch_user(user_id)

    vip_role = guild.get_role(VIP_ROLE_ID)
    is_vip = vip_role in member.roles if vip_role else False

    final_price = int(ราคา * 0.8) if is_vip else ราคา

    order_id = str(random.randint(1000, 9999))

    orders = load("orders.json")
    orders[order_id] = {
        "user_id": user_id,
        "สินค้า": สินค้า,
        "จำนวน": จำนวน,
        "ราคา": final_price,
        "status": "รอดำเนินการ"
    }
    save("orders.json", orders)

    category = get_category(guild, ORDER_CATEGORY_NAME)

    order_channel = None
    if category:
        order_channel = await guild.create_text_channel(
            name=f"order-{order_id}",
            category=category
        )

    embed = discord.Embed(title=f"🛍️ ORDER #{order_id}", color=discord.Color.green())
    embed.add_field(name="👤 ลูกค้า", value=user.mention, inline=False)
    embed.add_field(name="📦 สินค้า", value=สินค้า, inline=False)
    embed.add_field(name="🔢 จำนวน", value=จำนวน, inline=False)
    embed.add_field(name="💰 ราคา", value=f"{final_price}", inline=False)

    await interaction.channel.send(embed=embed)

    if order_channel:
        await order_channel.send(embed=embed)

    await interaction.response.send_message("✅ สร้างออเดอร์แล้ว", ephemeral=True)

    # ================= POINTS =================
    points = load("points.json")
    uid = str(user_id)

    points[uid] = points.get(uid, 0) + 1
    save("points.json", points)

    await update_vip(member, points[uid])
    await log(f"🛍️ ORDER #{order_id} | VIP={is_vip} | {final_price}")

# ================= POINT SYSTEM =================
@tree.command(name="แต้ม")
async def my_points(interaction: discord.Interaction):

    data = load("points.json")
    await interaction.response.send_message(f"🎟️ แต้ม: {data.get(str(interaction.user.id), 0)}")

@tree.command(name="rank")
async def rank(interaction: discord.Interaction):

    data = load("points.json")
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    uid = str(interaction.user.id)
    rank = 0

    for i, (u, _) in enumerate(sorted_data, start=1):
        if u == uid:
            rank = i
            break

    await interaction.response.send_message(f"🏆 Rank #{rank}")

@tree.command(name="leaderboard")
async def leaderboard(interaction: discord.Interaction):

    data = load("points.json")
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

    text = ""
    for i, (uid, pts) in enumerate(sorted_data, start=1):
        text += f"{i}. <@{uid}> - {pts}\n"

    await interaction.response.send_message(embed=discord.Embed(
        title="🏆 Leaderboard",
        description=text,
        color=discord.Color.gold()
    ))

# ================= ADMIN POINTS =================
@tree.command(name="ตั้งแต้ม")
async def set_points(interaction: discord.Interaction, user: discord.Member, amount: int):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

    data = load("points.json")
    data[str(user.id)] = amount
    save("points.json", data)

    await update_vip(user, amount)

    await interaction.response.send_message("✅ ตั้งแต้มแล้ว")

@tree.command(name="เพิ่มแต้ม")
async def add_points(interaction: discord.Interaction, user: discord.Member, amount: int):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

    data = load("points.json")
    uid = str(user.id)

    data[uid] = data.get(uid, 0) + amount
    save("points.json", data)

    await update_vip(user, data[uid])

    await interaction.response.send_message("➕ เพิ่มแต้มแล้ว")

@tree.command(name="ลดแต้ม")
async def remove_points(interaction: discord.Interaction, user: discord.Member, amount: int):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

    data = load("points.json")
    uid = str(user.id)

    data[uid] = max(0, data.get(uid, 0) - amount)
    save("points.json", data)

    await update_vip(user, data[uid])

    await interaction.response.send_message("➖ ลดแต้มแล้ว")

@tree.command(name="resetแต้ม")
async def reset_points(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

    save("points.json", {})

    await interaction.response.send_message("🧹 รีเซ็ตแต้มแล้ว")

# ================= SETUP =================
@tree.command(name="setup_ticket")
async def setup_ticket(interaction: discord.Interaction):

    channel = client.get_channel(1494046169511235755)

    embed = discord.Embed(
        title="🎫 Ticket System",
        description="กดปุ่มเพื่อเปิด Ticket",
        color=discord.Color.green()
    )

    await channel.send(embed=embed, view=TicketView())

    await interaction.response.send_message("✅ ตั้งระบบแล้ว", ephemeral=True)

# ================= READY =================
@client.event
async def on_ready():
    await tree.sync()
    print("Bot Ready")

client.run(TOKEN)
