from explicit_eggs import explicit_eggs
from discord import File
import deepfrier
import random
import re


def palindrome_parse(message):
    message = message.content
    chars_to_keep = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    #print(f"Message: {message}")
    message_no_space = ''.join(ch for ch in message if ch in chars_to_keep)
    #print(f"Message no space: {message_no_space}")
    lower = message_no_space.lower()
    if len(message_no_space) > 3 and lower == lower[::-1] and ' ' in message:
        #print(f'"{lower} == {lower[::-1]}"')
        return {"message": f"\"{message}\" is a palindrome! Wow!"}
    message = ''.join(ch for ch in message if ch in chars_to_keep + ' ')
    for word in message.split(" "):
        if len(word) <= 3:
            continue
        
        lower = word.lower()

        if lower in ['level'] or lower != lower[::-1]:
            continue

        else:
            return {"message": f"{word} is a palindrome! Wow!"}


def either(message):
    message = message.content
    if not message.lower().startswith('either'):
        return

    message = message.split(' or ')
    first_word = message[0].split(' ')[0]
    if len(message) > 1:
        # Remove the first word, previously confirmed to be 'either'
        message[0] = ' '.join(message[0].split(' ')[1:])
        return {'message': '***__' + random.choice(message).upper() + '__***'}


def simple_responses(message):
    message = message.content

    # REEEEE
    if 'REEE' in message.upper():
        return {
            "file": File("resources/memes/REEEE.gif", filename="REEEE.gif")
        }
    
    # Rarted
    if re.sub(r'\W+', '', message).lower().endswith('rarted'):
        return {
            "message": "https://i.kym-cdn.com/entries/icons/mobile/000/025/554/jomannn.jpg",
            "name": "Joseph man9062",
        }

    # Pay respects
    if len(message) > 0:
        pay_respects = True
        for letter in message.lower():
            if letter != "f":
                pay_respects = False
                break
        if pay_respects:
            return { "message": "F"*50 }

    # A GAME THEORY
    if "just a theory" in message.lower():
        return {"message": "A GAME THEORY"}

    # Madlad
    if "madlad" in message.replace(" ", ''):
        return {"message": "https://i.imgur.com/E1UCCxX.jpg", "name": "Pewdiepie"}

    # GOD
    for string in ["god said", "god told me"]:
       if string in message.lower():
            return {"message":"I NEVER SAID THAT", "name": "GOD"}

    # smh
    if message.lower() == 'smh':
        return {"file": File("resources/memes/smh.png", filename="smh.png")}
    
    if 'number 15' in message.lower():
        return {"message": """Number 15: Burger king foot lettuce. The last thing you'd want in your Burger King burger is someone's foot fungus. But as it turns out, that might be what you get. A 4channer uploaded a photo anonymously to the site showcasing his feet in a plastic bin of lettuce. With the statement: "This is the lettuce you eat at Burger King." Admittedly, he had shoes on.

But that's even worse."""}


async def run(client, message):
    if message.author.id == client.user.id:
        return

    parses = [
        palindrome_parse, 
        either,
        simple_responses,
    ] + explicit_eggs

    previous_name = client.user.display_name

    for parse in parses:
        output = parse(message)
        if output == None:
            continue
        if "name" in output:
            await message.guild.me.edit(nick=output["name"])

        if "message" in output:
            await message.channel.send(output["message"])

        if "file" in output:
            await message.channel.send(file=output["file"])

        if "name" in output:
            await message.guild.me.edit(nick=previous_name)

        if output:
            return

