import discord
from stock import reduce_stock
from order import create_order
from order_channel import get_order_channel

ORDER_DATA = {}  # เก็บ user ของแต่ละ order


class OrderModal(discord.ui.Modal, title="🛒 สั่งของ"):

    item = discord.ui.TextInput(label="สิ่งที่ต้องการสั่ง")
    qty = discord.ui.TextInput(label="จำนวน")

    async def on_submit(self, interaction: discord.Interaction):

        item = self.item.value
        qty = int(self.qty.value)

        price = 100 * qty

        if not reduce_stock(item, qty):
            return await interaction.response.send_message("❌ ของไม่พอ", ephemeral=True)

        oid = create_order(interaction.user.id, item, qty, price)

        ORDER_DATA[oid] = interaction.user.id  # เก็บ user

        channel = await get_order_channel(interaction.guild, oid)

        await channel.send(
            f"📦 Order #{oid}\n"
            f"👤 {interaction.user.mention}\n"
            f"🛒 {item}\n"
            f"🔢 {qty}\n"
            f"💰 {price}",
            view=OrderStatusView(oid)
        )

        await interaction.response.send_message(
            f"✅ สั่งของสำเร็จ #{oid}",
            ephemeral=True
        )


class OrderStatusView(discord.ui.View):

    def __init__(self, oid):
        super().__init__()
        self.oid = oid

    async def send_dm(self, interaction, status):

        user_id = ORDER_DATA.get(self.oid)

        if user_id:
            user = await interaction.client.fetch_user(user_id)

            try:
                await user.send(
                    f"📦 Order #{self.oid}\n"
                    f"🔔 สถานะอัปเดต: {status}"
                )
            except:
                pass

    @discord.ui.button(label="📥 รับออเดอร์", style=discord.ButtonStyle.green)
    async def accept(self, interaction, button):
        await self.update(interaction, "📥 รับออเดอร์แล้ว")

    @discord.ui.button(label="⛏ กำลังฟาร์ม", style=discord.ButtonStyle.blurple)
    async def farm(self, interaction, button):
        await self.update(interaction, "⛏ กำลังฟาร์ม")

    @discord.ui.button(label="📦 รอส่ง", style=discord.ButtonStyle.gray)
    async def wait(self, interaction, button):
        await self.update(interaction, "📦 รอส่ง")

    @discord.ui.button(label="✅ ส่งแล้ว", style=discord.ButtonStyle.green)
    async def done(self, interaction, button):
        await self.update(interaction, "✅ ส่งแล้ว")

    async def update(self, interaction, status):

        await self.send_dm(interaction, status)

        await interaction.channel.send(
            f"🔔 Order #{self.oid} → **{status}**"
        )

        await interaction.response.send_message(
            "อัปเดตแล้ว + DM แล้ว",
            ephemeral=True
        )
