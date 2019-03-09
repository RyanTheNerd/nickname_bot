import discord
import config
import random
import logging
import asyncio
import os

import name_parses
import easter_eggs

from database import get_nickname

from memegenerator import make_meme
from memegen_parses import MEMEGEN_PARSES
from utils import fade_messages

MEMEGEN_OUTPUT = "./temp/"
MEME_PATH = "./resources/memes/"
PREFIX = "/"

# This starts mongodb
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
    print(f"Servers:")
    for server in client.servers:
        print(f"\tserver.name")
    game = discord.Game(name=f"Confusing {member_count} users on {server_count} servers")
    await client.change_presence(game=game)
    await whats_new()
    #await send_palindrome()

# on_message runs every time the bot recieves a message from any channel
@client.event
async def on_message(message):
    author = message.author
    nickname = get_nickname(author.id, author.display_name)
    await change_nickname(author, nickname)
    await top_kek(message)
    client_message = None
    time = -1

    user, command, nickname = parse_request(message)

    await name_parses.run(client, message, user, command, nickname, message.channel)
    await easter_eggs.run(client, message)


    if command in MEMEGEN_PARSES:
        await memegen_parse(command, nickname, message)

    if client_message != None:
        if time == -1:
            await fade_messages(client, [client_message, message])
        else:
            await fade_messages(client, [client_message, message], time)




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
            user_name = client.get_user_info(user_id)
            user = message.server.get_member(user_id)

            nickname = " ".join(args[2:])


        if user == None:
            user = author
            user_name = "Same as author"
            user_id = author_id
            nickname = " ".join(args[1:])

        print(f"\tUser: {user_name}, ID: {user_id}")
        print(f"\tCommand: {command}, Nickname/Arg: {nickname or 'None'}")

    return user, command, nickname

async def change_nickname(author, nickname):
    try:
        await client.change_nickname(author, nickname)

    except Exception as e:
        print(f"Error changing {author.display_name}'s nickname: {e}")




async def top_kek(message):
    if "top kek" in message.content.lower():
        await client.send_file(message.channel, os.path.join(MEME_PATH, "top_kek.jpg"))

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
                    channel.type == discord.ChannelType.text):
                await client.send_message(channel, message)
                # So that we don't send to every channel:
                break

async def send_palindrome():
    # TODO
    with open("resources/shuffled_palindromes.txt", "r") as pal_file:
        pals = pal_file.read().split('\n')
        index = int(pals[-1])

    await client.send_message(client.get_channel("517190316273696768"), palindrome)

async def memegen_parse(meme, text, message):
    channel = message.channel
    lines = text.split(',')
    for line in range(len(lines)):
        lines[line] = lines[line].upper().strip()
    if len(lines) < 2:
        lines.append('')
    print(f"Generating {meme} meme: {lines[0]}, {lines[1]}")
    make_meme(lines[0], lines[1], meme)
    await client.send_file(channel, os.path.join(MEMEGEN_OUTPUT, f"{meme}.jpg"))
    await client.delete_message(message)

# This starts the bot 
client.run(config.token)
