import discord
import json
import asyncio
from shop import ShopView
from order import update_status
from logs import send_log

config = json.load(open("config.json"))

# เก็บ activity ของ ticket
active_time = {}

class TicketView(discord.ui.View):

    @discord.ui.button(label="🛒 สร้าง Ticket", style=discord.ButtonStyle.green)
    async def create(self, interaction, button):

        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(
            guild.categories,
            id=config["ticket_category_id"]
        )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites
        )

        active_time[channel.id] = asyncio.get_event_loop().time()

        await channel.send("🎫 Ticket เปิดแล้ว", view=TicketControlView())

        interaction.client.loop.create_task(auto_close(channel))

        await interaction.response.send_message(
            f"Ticket: {channel.mention}",
            ephemeral=True
        )


class TicketControlView(discord.ui.View):

    @discord.ui.button(label="🛒 เปิดร้าน", style=discord.ButtonStyle.green)
    async def shop(self, interaction, button):

        active_time[interaction.channel.id] = asyncio.get_event_loop().time()

        await interaction.channel.send("🛒 ร้านค้า", view=ShopView())
        await interaction.response.send_message("เปิดร้านแล้ว", ephemeral=True)


    @discord.ui.button(label="📦 ส่งของ", style=discord.ButtonStyle.blurple)
    async def send_item(self, interaction, button):

        channel = interaction.channel
        user = interaction.user

        # ใช้ order ล่าสุดจาก shop view (ปลอดภัยขึ้น)
        oid = str(load_latest_order())

        update_status(oid, "📦 ส่งแล้ว")

        try:
            await user.send(f"📦 Order #{oid} ส่งแล้ว")
        except:
            pass

        await send_log(interaction.client, f"📦 ส่ง #{oid}")

        await interaction.response.send_message("ส่งแล้ว", ephemeral=True)
        await channel.delete()


# 📌 AUTO CLOSE ฉลาดขึ้น
async def auto_close(channel):

    while True:

        await asyncio.sleep(60)

        last = active_time.get(channel.id, 0)

        now = asyncio.get_event_loop().time()

        # ถ้าไม่มีคนคุย 20 นาที
        if now - last > 1200:

            try:
                await channel.send("⏳ ไม่มีการใช้งาน 20 นาที → ปิด Ticket")
                await channel.delete()
            except:
                pass
            break
