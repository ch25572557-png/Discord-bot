import discord
from stock import add_stock, reduce_stock, load as stock_load

class AddStockModal(discord.ui.Modal, title="➕ เพิ่มสต๊อก"):

    item = discord.ui.TextInput(label="ชื่อสินค้า")
    qty = discord.ui.TextInput(label="จำนวน")

    async def on_submit(self, interaction: discord.Interaction):

        add_stock(self.item.value, int(self.qty.value))

        await interaction.response.send_message(
            f"➕ เพิ่ม {self.item.value} +{self.qty.value}",
            ephemeral=True
        )


class RemoveStockModal(discord.ui.Modal, title="➖ ลดสต๊อก"):

    item = discord.ui.TextInput(label="ชื่อสินค้า")
    qty = discord.ui.TextInput(label="จำนวน")

    async def on_submit(self, interaction: discord.Interaction):

        ok = reduce_stock(self.item.value, int(self.qty.value))

        if not ok:
            return await interaction.response.send_message(
                "❌ ของไม่พอหรือไม่มีสินค้า",
                ephemeral=True
            )

        await interaction.response.send_message(
            f"➖ ลด {self.item.value} -{self.qty.value}",
            ephemeral=True
        )


class AdminStockView(discord.ui.View):

    @discord.ui.button(label="➕ เพิ่มสต๊อก", style=discord.ButtonStyle.green)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(AddStockModal())


    @discord.ui.button(label="➖ ลดสต๊อก", style=discord.ButtonStyle.red)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(RemoveStockModal())


    @discord.ui.button(label="📊 ดูสต๊อก", style=discord.ButtonStyle.blurple)
    async def show(self, interaction: discord.Interaction, button: discord.ui.Button):

        data = stock_load()

        if not data:
            return await interaction.response.send_message("ไม่มีสินค้า", ephemeral=True)

        text = "\n".join(
            f"{k} | stock: {v['stock']}"
            for k, v in data.items()
        )

        await interaction.response.send_message(text, ephemeral=True)
