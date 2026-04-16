import discord
from order import load, save
from stock import load as sl, save as ss

class StatusView(discord.ui.View):

    def __init__(self, oid):
        super().__init__()
        self.oid = oid

    @discord.ui.button(label="❌ ยกเลิก", style=discord.ButtonStyle.danger)
    async def cancel(self,i,b):

        db = load()

        o = db["data"][self.oid]

        stock = sl()

        stock[o["item"]]["stock"] += o["qty"]
        ss(stock)

        del db["data"][self.oid]
        save(db)

        await i.response.send_message("ยกเลิกแล้ว",ephemeral=True)

    @discord.ui.button(label="🟢 ส่งแล้ว", style=discord.ButtonStyle.success)
    async def done(self,i,b):

        db = load()

        db["data"][self.oid]["status"] = "ส่งแล้ว"
        save(db)

        await i.response.send_message("ส่งแล้ว",ephemeral=True)

        await i.channel.delete()
