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
TICKET_CATEGORY_ID = 1494046169511235755
ORDER_CATEGORY_ID = 1494062876334358739
LOG_CHANNEL_ID = 1494258803422662856

VIP_ROLE_ID = 0

tickets = {}

# ================= LOAD / SAVE =================
def load(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ================= SAFE GET CATEGORY =================
def get_category(guild, cid):
    ch = guild.get_channel(cid)
    return ch if isinstance(ch, discord.CategoryChannel) else None

# ================= LOG =================
async def log(msg):
    ch = client.get_channel(LOG_CHANNEL_ID)
    if ch:
        await ch.send(msg)

# ================= TICKET =================
class TicketView(discord.ui.View):

    @discord.ui.button(label="🎫 เปิด Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        category = get_category(guild, TICKET_CATEGORY_ID)

        if not category:
            return await interaction.response.send_message(
                "❌ Ticket category ไม่ถูกต้อง",
                ephemeral=True
            )

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

        await interaction.response.send_message(
            f"🎫 เปิด Ticket แล้ว: {channel.mention}",
            ephemeral=True
        )

        await channel.send("🛍️ ใช้ /ส่งของ ในห้องนี้")

# ================= GET USER =================
def get_ticket_user(channel_id):
    return tickets.get(channel_id)

# ================= ORDER =================
@tree.command(name="ส่งของ")
async def send_order(interaction: discord.Interaction, สินค้า: str, จำนวน: str, ราคา: int):

    user_id = get_ticket_user(interaction.channel.id)

    if not user_id:
        return await interaction.response.send_message("❌ ใช้ได้เฉพาะใน Ticket", ephemeral=True)

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
        "ราคา": final_price
    }
    save("orders.json", orders)

    # ================= ORDER CATEGORY =================
    category = get_category(guild, ORDER_CATEGORY_ID)

    order_channel = None
    if category:
        order_channel = await guild.create_text_channel(
            name=f"order-{order_id}",
            category=category
        )

    embed = discord.Embed(
        title=f"🛍️ ORDER #{order_id}",
        color=discord.Color.green()
    )

    embed.add_field(name="👤 ลูกค้า", value=user.mention, inline=False)
    embed.add_field(name="📦 สินค้า", value=สินค้า, inline=False)
    embed.add_field(name="🔢 จำนวน", value=จำนวน, inline=False)
    embed.add_field(name="💰 ราคา", value=f"{final_price} บาท", inline=False)

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

# ================= VIP =================
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

# ================= SETUP =================
@tree.command(name="setup_ticket")
async def setup_ticket(interaction: discord.Interaction):

    ch = client.get_channel(TICKET_CATEGORY_ID)

    await ch.send(
        embed=discord.Embed(
            title="🎫 Ticket System",
            description="กดปุ่มเพื่อเปิด Ticket",
            color=discord.Color.green()
        ),
        view=TicketView()
    )

    await interaction.response.send_message("✅ ตั้งบอร์ดแล้ว", ephemeral=True)

# ================= READY =================
@client.event
async def on_ready():
    await tree.sync()
    print("Bot Ready")

client.run(TOKEN)
