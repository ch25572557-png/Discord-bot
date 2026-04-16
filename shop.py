import discord

from stock import reduce_stock, get_price
from order import create_order
from points import add_points
from discount import get_discount
from order_channel import get_order_channel


class ShopView(discord.ui.View):

    @discord.ui.button(label="🛒 Buy", style=discord.ButtonStyle.green)
    async def buy(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_id = interaction.user.id
        item = "cash"

        # 1) ราคา
        price = get_price(item)

        # 2) discount
        discount = get_discount(user_id)
        final_price = price - (price * discount)

        # 3) เช็ค stock
        if not reduce_stock(item, 1):
            return await interaction.response.send_message("❌ ของหมด", ephemeral=True)

        # 4) สร้าง order
        order_id = create_order(user_id, item, 1, final_price)

        # 5) เพิ่ม points
        add_points(user_id, 1)

        # 6) สร้างห้อง order
        channel = await get_order_channel(interaction.guild, order_id)

        if channel:
            await channel.send(
                f"🆕 Order #{order_id}\n"
                f"👤 User: {interaction.user}\n"
                f"💰 Price: {final_price}"
            )

        # 7) ตอบกลับ user
        await interaction.response.send_message(
            f"✅ สั่งซื้อสำเร็จ Order #{order_id}",
            ephemeral=True
        )
