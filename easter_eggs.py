from explicit_eggs import explicit_eggs

def god_parse(message):
    message = message.content
    for string in ["god said", "god told me"]:
        if string in message.lower():
            return {"message":"I NEVER SAID THAT", "name": "GOD"}

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


#def dennis_parse(message):
#    if message.content.lower().startswith("no u"):
#        return {"delete": True}

def madlad(message):
    message = message.content
    if "madlad" in message.replace(" ", ''):
        return {"message": "https://i.imgur.com/E1UCCxX.jpg", "name": "Pewdiepie"}

def A_GAME_THEORY(message):
    message = message.content
    if "just a theory" in message.lower():
        return {"message": "A GAME THEORY"}

def john(message):
    message = message.content
    if "smh" in message:
        return {"message": "John is disappoint"}

def pay_respects(message):
    message = message.content
    if len(message) == 0:
        return
    for letter in message:
        if letter != "f":
            return
    return { "message": "f"*50 }

async def run(client, message):
    if message.author.id == client.user.id:
        return

    parses = [
        madlad, 
        john, 
        god_parse, 
        pay_respects,
        palindrome_parse, 
        A_GAME_THEORY,
#        dennis_parse,
    ] + explicit_eggs
    previous_name = client.user.display_name

    for parse in parses:
        output = parse(message)
        if output == None:
            continue
        if "delete" in output:
            await client.delete_message(message)
        if "name" in output:
            await client.change_nickname(message.server.me, output["name"])

        if "message" in output:
            await client.send_message(message.channel, output["message"])

        if "name" in output:
            await client.change_nickname(message.server.me, previous_name)

        if output:
            return

