import discord
import config
import random
import logging
import database as db


name = "billy"

# This creates an instance of the bot
client = discord.Client()

# on_ready function is only ran when the bot is first started
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ')')
    print('Connected to ' + str(len(client.servers)) + ' servers')
    print('Connected to ' + str(len(set(client.get_all_members()))) + ' users')

# on_message runs every time the bot recieves a message from any channel
@client.event
async def on_message(message):
    author = message.author
    for string in ["god said", "god told me"]:
        if string in message.content.lower():
            await client.change_nickname(message.server.me, "GOD")
            await client.send_message(message.channel, "I NEVER SAID THAT")
            await client.change_nickname(client.user, previous_name)
    nickname = db.get_nickname(author.id, author.display_name)
    try:
        await client.change_nickname(author, nickname)
    except:
        print(f"I can't change {author.display_name}'s nickname")

    user, function, nickname = parse_request(message)

    if function == "/addname":
        print(f"\tAdding Name for {user}: {nickname}")
        response = db.add_nickname(user.id, nickname)
        if len(response) != 0:
            await client.send_message(message.channel, response)

    elif function == "/rmname":
        print(f"Removing Name {nickname} from {user.display_name}'s bank")
        db.remove_nickname(user.id, nickname)
        
    elif function == "/lsname":
        print("\tListing Names:")
        await client.send_message(message.channel, db.pprint_names(user.id))
    
    elif function == "/cls":
        print("Deleting previous messages")

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


# accepts a message object
# returns user, function, and nickname
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
        print(f"\tChanging {author.display_name}'s nickname to {nickname}")
    except discord.errors.Forbidden:
        print("Forbidden")
    return nickname 

# This starts the bot
client.run(config.token)


