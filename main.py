import discord
import config
import random
import logging
import asyncio
import string
import os

import name_parses
import easter_eggs

from database import db

from memegenerator import make_meme
from memegen_parses import MEMEGEN_PARSES
from utils import fade_messages
from config import PREFIX
from fight import fight
#from question import quiz_client

MEMEGEN_OUTPUT = "./temp/"
MEME_PATH = "./resources/memes/"

# This starts mongodb
# This creates an instance of the bot
client = discord.Client()

# on_ready function is only ran when the bot is first started
@client.event
async def on_ready():
    member_count = len(set(client.users))
    guild_count = len(client.guilds)
    print(f"Logged in as {client.user.name} (ID: {client.user.id})")
    print(f"Over {db.count_nicknames()} saved nicknames")
    print(f"Connected to {guild_count} guilds")
    print(f"Connected to {member_count} users")
    print(f"guilds:")
    for guild in client.guilds:
        print(f"\t{guild.name}")
    status = discord.Game(name=f"Over {db.count_nicknames()} saved nicknames")
    await client.change_presence(activity=status)
    #await whats_new()
    #await send_palindrome()

# on_message runs every time the bot recieves a message from any channel
@client.event
async def on_message(message):
    author = message.author
    nickname = db.get_nickname(author.id, author.display_name)
    await change_nickname(message, author, nickname)

    user, command, nickname = parse_request(message)

    #await top_kek(message)
    await name_parses.run(client, message, user, command, nickname, message.channel)
    await easter_eggs.run(client, message)
    await fight(message)
    #await quiz_client.handle_message(client, message)

    if command in MEMEGEN_PARSES:
        await memegen_parse(command, nickname, message)





# accepts a message object
# returns user object, command name, and nickname
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

async def change_nickname(message, author, nickname):
    try:
        await author.edit(nick=nickname)

    except Exception as e:
        if message.guild.owner == author:
            return
        print(f"Error changing {author.display_name}'s nickname: {e}")




async def top_kek(message):
    if "top kek" in message.content.lower():
        await message.channel.send(file=os.path.join(MEME_PATH, "top_kek.jpg"))

async def whats_new():
    with open("resources/whats_new.txt", 'a+') as message_file:
        message_file.seek(0, 0)
        message = message_file.read()
        if message.endswith("already_announced"):
            return
        message_file.seek(0, 2)
        message_file.write("already_announced")

    # Post message in first text channel with write permission in each guild

    for guild in client.guilds: 
        # Spin through every guild
        for channel in guild.channels: 
            # Channels on the guild
            if (channel.permissions_for(guild.me).send_messages and 
                    channel.type == discord.ChannelType.text):
                await channel.send(message)
                # So that we don't send to every channel:
                break

async def memegen_parse(meme, text, message):
    channel = message.channel
    lines = text.split(',')
    for line in range(len(lines)):
        lines[line] = lines[line].upper().strip()
    if len(lines) < 2:
        lines.append('')
    print(f"Generating {meme} meme: {lines[0]}, {lines[1]}")
    make_meme(lines[0], lines[1], meme)
    await channel.send(file=discord.File(os.path.join(MEMEGEN_OUTPUT, f"{meme}.jpg")))
    await message.delete()

client.run(config.token)
