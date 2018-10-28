import discord
import config
import random

# pool is a dictionary filled with keys of user id's pointing to a 
# corresponding pool of nicknames
pool = {}

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
        user, function, nickname = parse_request(message); 
        await change_nickname(message.author)

        if function == "/addname":
            print(f"\tAdding Name:")
            print(f"New nickname for {user}: {nickname}")
            add_nickname(user, nickname)

        elif function == "/rmname":
            print(f"Removing nickname {nickname} from {user.display_name}'s bank")
            remove_nickname(user, nickname)
            
        elif function == "/lsname":
            print("\tListing Names:")
            await list_names(user, message.channel)


# accepts a message object
# returns user, function, and nickname
def parse_request(message):
    author = message.author
    user = None
    function = None
    nickname = None
    init_pool(author)

    if message.content.startswith("/"):
        args = message.content.split(" ")
        function = args[0]
        print("Author:",message.author.display_name)

        if len(args) > 1:
            user_id = ''.join(i for i in args[1] if i.isdigit())
            print(f"User id: {user_id}")
            user = message.server.get_member(user_id)

            init_pool(user)
            nickname = " ".join(args[2:])

        if user == None:
            user = author
            nickname = " ".join(args[1:])
            print("\tNo user specified, using Author instead")

    return user, function, nickname


async def change_nickname(author):
    nickname = pool[author.id][random.randrange(len(pool[author.id]))]
    try:
        print(f"\tChanging {author.display_name}'s nickname to {nickname}")
        await client.change_nickname(author, nickname)
    except discord.errors.Forbidden:
        print("Error: Forbidden")
    return nickname 

def remove_nickname(user, nickname):
    try:
        pool[user.id].pop(int(nickname)-1)
    except:
        print("Index of nickname is out of range lol")

def add_nickname(author, nickname):
    pool[author.id].append(nickname)


async def list_names(user, channel):
    names = pool[user.id]
    names = ", ".join(names)
    print(names)
    await client.send_message(channel, names)

def init_pool(author):
    if author.id not in pool:
        print(f"Adding {author.display_name} to the pool.")
        pool[author.id] = []
        pool[author.id].append(author.display_name)

# This starts the bot
client.run(config.token)
