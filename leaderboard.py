import discord
from points import load

class LeaderboardView(discord.ui.View):

    @discord.ui.button(label="🏆 Top Points", style=discord.ButtonStyle.blurple)
    async def show(self, interaction, button):

        data = load()
        top = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

        text = "\n".join([f"{i+1}. {u} - {p}" for i,(u,p) in enumerate(top)])

        await interaction.response.send_message(text or "no data", ephemeral=True)
