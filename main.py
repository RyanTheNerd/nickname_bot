import discord
import config
import random
import logging
import asyncio

import datetime as dt
import database as db

from memegenerator import alex_jones
from parses import extra_parses

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
    await whats_new()
    #await send_palindrome()

# on_message runs every time the bot recieves a message from any channel
@client.event
async def on_message(message):
    author = message.author
    nickname = db.get_nickname(author.id, author.display_name)
    await change_nickname(author, nickname)
    await top_kek(message)
    client_message = None
    time = None

    user, function, nickname = parse_request(message)
    await extra_parses(client, message)

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
                "\t`/addname @Xtgyuio kek` - adds the name `kek` to Xtgyuio's pool\n"
                "\t`/rmname potato` - remove the name `potato` from your pool\n"
                "\t`/lsname` - list all current names in your pool\n"
                "You get the idea"
        )
        await client.send_message(message.channel, help_message)
    elif function in ["/cls", "/clr"]:
        print(f"Clearing messages for channel '{str(message.channel)}'")
        client_message = await client.send_message(message.channel, 
                await clear_messages(message.channel))

    elif function == "/alexjones":
        nickname = nickname.upper() 
        lines = nickname.split(',')
        lines[0] = lines[0].strip()
        lines[1] = lines[1].strip()
        if len(lines) < 2:
            lines.append('')
        print(f"Generating Alex Jones meme: {lines[0]}, {lines[1]}")
        alex_jones(lines[0], lines[1])
        await client.send_file(message.channel, "temp/alex_jones.jpg")

    if client_message != None:
        await fade_messages([client_message, message], time)


# accepts a message object
# returns user object, function name, and nickname
def parse_request(message):
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
    except discord.errors.Forbidden:
        print(f"I can't change {author.display_name}'s nickname")


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

async def top_kek(message):
    if "top kek" in message.content.lower():
        await client.send_file(message.channel, "resources/top-kek-2.png")

async def whats_new():
    with open("resources/whats_new.txt", 'a+') as message_file:
        message_file.seek(0, 0)
        message = message_file.read()
        if message.endswith("already_announced"):
            return
        message_file.seek(0, 2)
        message_file.write("already_announced")

    # Post message in first text channel with write permission in each server

    for server in client.servers: 
        # Spin through every server
        for channel in server.channels: 
            # Channels on the server
            if (channel.permissions_for(server.me).send_messages and 
                    channel.type == "text"):
                await client.send_message(channel, message)
                # So that we don't send to every channel:
                break
async def send_palindrome():
    # TODO
    with open("resources/shuffled_palindromes.txt", "r") as pal_file:
        pals = pal_file.read().split('\n')
        index = int(pals[-1])

    await client.send_message(client.get_channel("517190316273696768"), palindrome)


# This starts the bot 
client.run(config.token)
