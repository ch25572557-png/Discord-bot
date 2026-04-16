import discord
import json

from stock import add_stock, reduce_stock, load as stock_load
from points import add_points

config = json.load(open("config.json"))
ADMIN_ROLE_ID = config["admin_role_id"]


def is_admin(interaction):
    return any(r.id == ADMIN_ROLE_ID for r in interaction.user.roles)


class AddStockModal(discord.ui.Modal, title="เพิ่มสต๊อก"):
    item = discord.ui.TextInput(label="สินค้า")
    qty = discord.ui.TextInput(label="จำนวน")

    async def on_submit(self, interaction):
        add_stock(self.item.value, int(self.qty.value))
        await interaction.response.send_message("เพิ่มแล้ว", ephemeral=True)


class RemoveStockModal(discord.ui.Modal, title="ลดสต๊อก"):
    item = discord.ui.TextInput(label="สินค้า")
    qty = discord.ui.TextInput(label="จำนวน")

    async def on_submit(self, interaction):
        reduce_stock(self.item.value, int(self.qty.value))
        await interaction.response.send_message("ลดแล้ว", ephemeral=True)


class AdminStockView(discord.ui.View):

    @discord.ui.button(label="➕", style=discord.ButtonStyle.green)
    async def add(self, interaction, button):

        if not is_admin(interaction):
            return await interaction.response.send_message("❌ admin only", ephemeral=True)

        await interaction.response.send_modal(AddStockModal())

    @discord.ui.button(label="➖", style=discord.ButtonStyle.red)
    async def remove(self, interaction, button):

        if not is_admin(interaction):
            return await interaction.response.send_message("❌ admin only", ephemeral=True)

        await interaction.response.send_modal(RemoveStockModal())

    @discord.ui.button(label="📊", style=discord.ButtonStyle.blurple)
    async def show(self, interaction, button):

        if not is_admin(interaction):
            return await interaction.response.send_message(str(stock_load()), ephemeral=True)


class AdminPointsView(discord.ui.View):

    @discord.ui.button(label="➕ Points", style=discord.ButtonStyle.green)
    async def add(self, interaction, button):

        if not is_admin(interaction):
            return await interaction.response.send_message("❌ admin only", ephemeral=True)

        await interaction.response.send_message("user_id amount", ephemeral=True)

        msg = await interaction.client.wait_for("message")
        uid, amt = msg.content.split()

        add_points(uid, int(amt))

        await interaction.channel.send("เพิ่มแต้มแล้ว")
