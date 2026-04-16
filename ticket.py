import discord
import json
from shop import ShopView
from logs import send_log
from order import load, save

config = json.load(open("config.json"))

class TicketControlView(discord.ui.View):

    @discord.ui.button(label="🛒 เปิดร้าน", style=discord.ButtonStyle.green)
    async def shop(self, interaction, button):
        await interaction.channel.send("🛒 ร้านค้า", view=ShopView())
        await interaction.response.send_message("เปิดร้านแล้ว", ephemeral=True)


    @discord.ui.button(label="📦 ส่งของ", style=discord.ButtonStyle.blurple)
    async def send_item(self, interaction, button):

        channel = interaction.channel
        user = interaction.user

        # 📦 อัปเดต order status (ตัวล่าสุด)
        db = load()

        last_id = str(db["counter"])
        if last_id in db["data"]:
            db["data"][last_id]["status"] = "📦 ส่งแล้ว"
            save(db)

        # 🧾 DM ลูกค้า (ใบเสร็จ)
        try:
            await user.send(
                f"📦 สินค้าของคุณถูกส่งแล้ว\n"
                f"🧾 Order #{last_id}\n"
                f"💙 ขอบคุณที่ใช้บริการ"
            )
        except:
            pass

        # 📊 log
        await send_log(
            interaction.client,
            f"📦 ส่งของ | Order #{last_id} | ห้อง {channel.name} | ลูกค้า {user}"
        )

        await interaction.response.send_message("✅ ส่งของแล้ว กำลังปิด Ticket...", ephemeral=True)

        # ❌ ปิด ticket
        await channel.delete()
