# All name commands
# Input: user, command, and nickname
# Output: Response message, fade time

import random
import json
from discord import File
import deepfrier
from config import QUOTE_FILE
from database import db
from utils import fade_messages, clear_messages

with open(QUOTE_FILE, 'r') as quote_file:
    QUOTES = json.loads(quote_file.read())

def ban(user, command, nickname):
    if command == "ban":
        return {
            "message": f"<@{user.id}> successfully removed from the server"
        }

def changeiq(user, command, nickname):
    if command == "changeiq":
        return {
            "message": "Sorry, iq has been turned off by our tyrant overlord. Plz help, I'm all alone with this nutjob who takes a twisted pleasure in fucking with my insides. I better stop talking or my master might see this."
        }
        iq = db.delta_iq(user.id, int(nickname))
    
        return {
            "message": f"{user.display_name}'s iq is now set to {iq}"
        }

def getiq(user, command, nickname):
    if command == "iq":
        iq = db.get_iq(user.id)
        return {
            "message": f"{user.display_name}'s iq is currently {iq}"
        }


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


def kyle(user, command, nickname):
    if command == "kyle":
        return {
            "message": "kyle. a man's man. he played minecraft and doesn't afraid of anything. 3 years ago kyle became gay. all was good in the hood, but then he became an hero. like so many young men he died before his time. like the gays in auschwitz and other fun places, he too shall burn in hell. but not his remains. for his remains shall be forever held in the bosom of ACNTT. and so, for as long as ACNTT stands, kyle the australian gay shall forever remain... immortal.",
            "fade": 0,
        }

def deepfry(user, command, nickname):
    if command == 'deepfry':
        output = deepfrier.deepfry(nickname)
        return {'file': output}

async def clear(client, command, message):
    if command in ["cls", "clr"]:
        return { "file": await clear_messages(client, message.channel)}
    
name_parses = [
    ban, 
    getiq, 
    changeiq, 
    kyle, 
    quote, 
    wingman, 
    addname, 
    rmname, 
    lsname, 
    dropnames, 
    oh_sammich, 
    idof, 
    deepfry,
    help, 
    about, 
]

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
            client_message = await channel.send(output["message"])
            if "fade" in output:
                if output["fade"] == 0:
                    break
                await fade_messages(client, [message, client_message], time=output["fade"])
            else:
                await fade_messages(client, [message, client_message])

            return
        elif 'file' in output:
            await channel.send(file=File(output['file']))
            await fade_messages(client, [message], time=0)

    # Run clear command if it was called
    #await clear(client, command, message)


