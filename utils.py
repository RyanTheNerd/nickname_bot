import asyncio
import datetime as dt
PREFIX = "/"
async def fade_messages(client, messages, time=3):
    await asyncio.sleep(time)
    for message in messages:
        try:
            await client.delete_message(message)
        except:
            continue
async def clear_messages(client, channel):
    def predicate(message):
        if(message.author == client.user):
            return True
        if message.content.startswith(PREFIX):
            return True
        return False

    time = dt.datetime.utcnow() - dt.timedelta(days=5)
    removed = len(await client.purge_from(channel, check=predicate, after=time))
    return (f"{removed} messages successfully removed.")
