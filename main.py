import discord
import config
import random
import logging
import asyncio
import datetime as dt
import database as db


name = "billy"

# This creates an instance of the bot
client = discord.Client()

# on_ready function is only ran when the bot is first started
@client.event
async def on_ready():
    member_count = len(set(client.get_all_members()))
    server_count = len(client.servers)
    print(f"Logged in as {client.user.name} (ID: {client.user.id})")
    print(f"Connected to {server_count} servers")
    print(f"Connected to {member_count} users")
    game = discord.Game(name=f"Confusing {member_count} users on {server_count} servers")
    await client.change_presence(game=game)

# on_message runs every time the bot recieves a message from any channel
@client.event
async def on_message(message):
    author = message.author
    nickname = db.get_nickname(author.id, author.display_name)
    client_message = None
    time = None
    await god_parse(message)
    await palindrome_parse(message)
    await change_nickname(author, nickname)

    user, function, nickname = parse_request(message)

    if function == "/addname":
        print(f"\tAdding Name for {user}: {nickname}")
        response = db.add_nickname(user.id, nickname)
        if len(response) != 0:
            client_message = await client.send_message(message.channel, response)
            time = 2

    elif function == "/rmname":
        print(f"Removing Name {nickname} from {user.display_name}'s bank")
        db.remove_nickname(user.id, nickname)
        client_message = await client.send_message(message.channel, 
                f"Removing Name {nickname} from {user.display_name}'s bank")
        time = 2
        
    elif function == "/lsname":
        print("\tListing Names:")
        client_message = await client.send_message(message.channel, 
                db.pprint_names(user.id))
        time = 7
    
    elif function == "/help":
        help_message = (
                "\t\tRandom nickname bot\n\n"
                "Commands:\n"
                "\t`/addname potato` - adds the name `potato` to your pool\n"
                "\t`/addname @Xtguio kek` - adds the name `kek` to Xtguio's pool\n"
                "\t`/rmname potato` - remove the name `potato` from your pool\n"
                "\t`/lsname` - list all current names in your pool\n"
                "You get the idea"
        )
        await client.send_message(message.channel, help_message)
    elif function in ["/cls", "/clr"]:
        print(f"Clearing messages for channel '{str(message.channel)}'")
        client_message = await client.send_message(message.channel, 
                await clear_messages(message.channel))

    if client_message != None:
        print(f"Client message: {client_message}")
        await fade_messages([client_message, message], time)


# accepts a message object
# returns user object, function name, and nickname
def parse_request(message):
    previous_name = client.user.display_name;
    author = message.author
    user = None
    function = None
    nickname = None

    if message.content.startswith("/"):
        args = message.content.split(" ")
        function = args[0]
        print(f"Author: {message.author.display_name}, ID: {message.author.id}")

        if len(args) > 1:
            user_id = ''.join(i for i in args[1] if i.isdigit())
            print(f"User id: {user_id}")
            user = message.server.get_member(user_id)

            nickname = " ".join(args[2:])

        if user == None:
            user = author
            nickname = " ".join(args[1:])
            print("\tNo user specified, using Author instead")

    return user, function, nickname


async def change_nickname(author, nickname):
    try:
        await client.change_nickname(author, nickname)
    except:
        print(f"I can't change {author.display_name}'s nickname")

async def god_parse(message):
    for string in ["god said", "god told me"]:
        if string in message.content.lower():
            await client.change_nickname(message.server.me, "GOD")
            await client.send_message(message.channel, "I NEVER SAID THAT")
            await client.change_nickname(client.user, previous_name)

async def fade_messages(messages, time):
    await asyncio.sleep(7)
    for message in messages:
        try:
            await client.delete_message(message)
        except:
            continue

async def clear_messages(channel):
    def predicate(message):
        if(message.author == client.user):
            return True
        for start in ["/lsname", "/rmname", "/addname", "/cls", "clr", "/help"]:
            if message.content.startswith(start):
                return True
        return False

    time = dt.datetime.utcnow() - dt.timedelta(days=5)
    removed = len(await client.purge_from(channel, check=predicate, after=time))
    return (f"{removed} messages successfully removed.")
async def palindrome_parse(message):
    if message.author != client.user:
        for word in message.content.split(" "):
            if len(word) > 2:
                lower = word.lower()
                if lower == lower[::-1]:
                    id_num = message.author.id
                    await client.send_message(message.channel, 
                            f"{word} is a palindrome! Wow!")
                    return

    

# This starts the bot 
client.run(config.token)
