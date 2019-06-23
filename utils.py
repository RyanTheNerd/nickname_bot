import asyncio
import datetime as dt
PREFIX = "/"
async def fade_messages(client, messages, time=3):
    await asyncio.sleep(time)
    for message in messages:
        try:
            await message.delete()
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

def parse_request(message):
    author = message.author
    user = None
    command = None
    nickname = None

    if message.content.startswith(PREFIX):
        args = message.content.split(" ")
        command = args[0][1:]
        author_name = message.author.display_name
        author_id = message.author.id
        print(f"Author: {author_name}, ID: {author_id}")

        if len(args) > 1: 
            user_id = ''.join(i for i in args[1] if i.isdigit())
            if len(user_id) is 18:
                user = message.guild.get_member(int(user_id))

        if user is None:
            user = author
            user_id = author_id
            user_name = "Same as Author"
            nickname = ' '.join(args[1:])

        else:
            user_name = user.display_name
            nickname = " ".join(args[2:])


        print(f"\tUser: {user_name}, ID: {user_id}")
        print(f"\tCommand: {command}, Nickname/Arg: {nickname}\n")

    return user, command, nickname

