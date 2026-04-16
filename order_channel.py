import discord
import json

config = json.load(open("config.json"))

async def get_order_channel(guild, oid):

    category = discord.utils.get(guild.categories, id=config["order_category_id"])

    for ch in category.channels:
        if ch.name == f"order-{oid}":
            return ch

    return await guild.create_text_channel(
        name=f"order-{oid}",
        category=category
    )
