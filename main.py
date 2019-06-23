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
from utils import fade_messages, parse_request
from config import PREFIX
from fight import fight
from animate import run_animations
from stats import genStatsHTML

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
    await genStatsHTML(client, db, config.STATSPATH)
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
    await run_animations(message)
    #await quiz_client.handle_message(client, message)

    if command in MEMEGEN_PARSES:
        await memegen_parse(command, nickname, message)





# accepts a message object
# returns user object, command name, and nickname
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

async def expire_names():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Checking for expired names...")
        db.expire_names()
        await asyncio.sleep(60*60)

client.loop.create_task(expire_names())

client.run(config.TOKEN)
