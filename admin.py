import discord
from stock import add_stock, reduce_stock, load as stock_load
from points import add_points

class AdminStockView(discord.ui.View):

    @discord.ui.button(label="➕ เพิ่มสต๊อก", style=discord.ButtonStyle.green)
    async def add(self, interaction, button):

        await interaction.response.send_message("item qty", ephemeral=True)
        msg = await interaction.client.wait_for("message")

        item, qty = msg.content.split()
        add_stock(item, int(qty))

        await interaction.channel.send(f"➕ {item} +{qty}")

    @discord.ui.button(label="➖ ลดสต๊อก", style=discord.ButtonStyle.red)
    async def remove(self, interaction, button):

        await interaction.response.send_message("item qty", ephemeral=True)
        msg = await interaction.client.wait_for("message")

        item, qty = msg.content.split()
        reduce_stock(item, int(qty))

        await interaction.channel.send(f"➖ {item} -{qty}")

    @discord.ui.button(label="📊 ดูสต๊อก", style=discord.ButtonStyle.blurple)
    async def show(self, interaction, button):

        data = stock_load()
        text = "\n".join([f"{k}: {v['stock']}" for k,v in data.items()])

        await interaction.response.send_message(text or "empty", ephemeral=True)


class AdminPointsView(discord.ui.View):

    @discord.ui.button(label="➕ Points", style=discord.ButtonStyle.green)
    async def add(self, interaction, button):

        await interaction.response.send_message("user_id amt", ephemeral=True)
        msg = await interaction.client.wait_for("message")

        uid, amt = msg.content.split()
        add_points(uid, int(amt))

        await interaction.channel.send(f"➕ {uid} +{amt}")
