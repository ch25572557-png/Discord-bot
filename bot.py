import discord
from discord.ext import commands
import json

from ticket import TicketView

# โหลด config
config = json.load(open("config.json", "r", encoding="utf-8"))

# intents (สำคัญมาก)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # สำคัญสำหรับ admin + dm + fetch user

bot = commands.Bot(command_prefix="!", intents=intents)


# -------------------------
# BOT READY
# -------------------------
@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")


# -------------------------
# สั่งเปิดระบบ ticket
# -------------------------
@bot.command()
async def panel(ctx):
    """ส่งปุ่มสั่งของ"""
    await ctx.send("🛒 กดปุ่มด้านล่างเพื่อสั่งของ", view=TicketView())


# -------------------------
# เช็คระบบ
# -------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


# -------------------------
# ERROR HANDLE
# -------------------------
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")


# -------------------------
# RUN BOT
# -------------------------
bot.run("YOUR_BOT_TOKEN")
