import discord
import json

from stock import reduce_stock, get_price
from points import add_points
from discount import get_discount
from order import create_order
from order_channel import get_order_channel


def load_config():
    return json.load(open("config.json"))


class ShopView(discord.ui.View):

    @discord.ui.button(label="🛒 Buy", style=discord.ButtonStyle.green)
    async def buy(self, interaction, button):

        config = load_config()

        item = "cash"

        price = get_price(item)
        discount = get_discount(interaction.user.id)
        final = price - (price * discount)

        if not reduce_stock(item, 1):
            return await interaction.response.send_message("❌ หมด", ephemeral=True)

        oid = create_order(interaction.user.id, item, 1, final)

        add_points(interaction.user.id, 1)

        # 📦 order channel
        ch = await get_order_channel(interaction.guild, oid)
        if ch:
            await ch.send(f"📦 Order #{oid}\n💰 {final}")

        # 🔔 admin log
        admin = interaction.guild.get_channel(config["admin_log_channel_id"])
        if admin:
            await admin.send(f"📦 ORDER #{oid} | {interaction.user} | {final}")

        # 📊 debug log
        check = interaction.guild.get_channel(config["check_log_channel_id"])
        if check:
            await check.send(f"[DEBUG] {interaction.user.id} {item} {final}")

        # 📩 DM
        try:
            await interaction.user.send(f"✅ Order #{oid}\n💰 {final}")
        except:
            pass

        await interaction.response.send_message(f"✅ #{oid}", ephemeral=True)
