async def send_log(client, text):

    import json
    config = json.load(open("config.json"))

    channel = client.get_channel(config["log_channel_id"])

    if channel:
        await channel.send(text)
