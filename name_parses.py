# All name commands
# Input: user, command, and nickname
# Output: Response message, fade time

import random
import json
import database as db
from utils import fade_messages, clear_messages

with open("quotes.json", 'r') as quote_file:
    QUOTES = json.loads(quote_file.read())['quotes']

def addname(user, command, nickname):
    if command == "addname":
        response = db.add_nickname(user.id, nickname)
        if len(response) != 0:
            return { "message": response }

def rmname(user, command, nickname):
    if command == "rmname":
        db.remove_nickname(user.id, nickname)
        return { 
            "message": f"Removing Name {nickname} from {user.display_name}'s bank"
        }
        
def lsname(user, command, nickname):
    if command in ["lsname", "lsarchived", "lsall"]:
        queries = {"lsarchived": "archived", "lsall": "all", "lsname": "default"}
        return { 
            "message": db.pprint_names(user.id, queries[command]), 
            "fade": 7
        }

def dropnames(user, command, nickname):
    if command == "dropnames":
        db.remove_all_names(user.id)
        return {
        "message": f"Successfully dropped all names for user {user.display_name}"
        }
def help(user, command, nickname):
    if command == "help":
        with open("./README.md", 'r') as README:
            return { "message": f"```md\n{README.read()}```", "fade": 30 }

def about(user, command, nickname):
    if command == "about":
        with open("./resources/about.txt", 'r') as about:
            return { "message": about.read() }

def oh_sammich(user, command, nickname):
    if command == "sammich":
        return { "message": "https://haggleforth.com/sammich", "fade": 10 }

def idof(user, command, nickname):
    if command == "idof":
        return { "message": f"ID of {user.display_name}: {user.id}", "fade": 10 }

def wingman(user, command, nickname):
    if command == "wingman":
        user = f"<@{user.id}>"
        return { "message": 
        random.choice([
f"This guy {user}, he may look autistic, but he's actually a genius",
f"{user} has a dick I think",
f"{user} is so sexy that no girl has ever had the guts to talk to him",
f"{user} has such a high libido that he faps to hentai 3 times daily",
f"{user} may be a virgin, but he's had lots of experience with his body pillows",
        ]),
        "fade": 0,
        }

def quote(user, command, nickname):
    if command == "quote":
        quote = random.choice(QUOTES)
        return {
            "message": f"\"{quote['quote']}\" - {quote['author']}",
            "fade": 0,
        }


async def clear(client, command, message):
    if command in ["cls", "clr"]:
        return { "message": await clear_messages(client, message.channel)}
    
name_parses = [quote, wingman, addname, rmname, lsname, dropnames, oh_sammich, idof, help, about]

async def run(client, message, user, command, nickname, channel):
    for function in name_parses:
        output = function(
            user = user, 
            command = command, 
            nickname = nickname, 
        )
        if output == None:
            continue
        if "message" in output:
            client_message = await client.send_message(channel, output["message"])
            if "fade" in output:
                if output["fade"] == 0:
                    break
                await fade_messages(client, [message, client_message], time=output["fade"])
            else:
                await fade_messages(client, [message, client_message])

            return

    # Run clear command if it was called
    await clear(client, command, message)


