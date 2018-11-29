import re
def yum_yum(message):
    # John contributed anal, butt, and butts
    yum = ['dick', 'dicks', 'penis', 'butthole', 'ass', 'anal', 'butt', 'butts'] 
    if message.lower() in yum:
        return {"message": "Yum yum"}
    for name in ['jacob', 'dennis', 'john', 'ryan', 'isaak']:
        if message.lower() == name:
            return {"message": f"{message} is a degenerate"}
def god_parse(message):
    for string in ["god said", "god told me"]:
        if string in message.lower():
            return {"message":"I NEVER SAID THAT", "name": "GOD"}

def palindrome_parse(message):
    chars_to_keep = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    message_no_space = ''.join(ch for ch in message if ch in chars_to_keep)
    lower = message_no_space.lower()
    if len(message) > 3 and lower == lower[::-1] and ' ' in message:
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

def dennis_parse(message):
    if message.lower().startswith("no u"):
        return {"message": "stfu dennis", "name": "Dennis' Mom"}

def A_GAME_THEORY(message):
    if "just a theory" in message.lower():
        return {"message": "A GAME THEORY"}

async def extra_parses(client, message):
    if message.author.id == client.user.id:
        return

    parses = [god_parse, palindrome_parse, dennis_parse, A_GAME_THEORY, yum_yum]
    previous_name = client.user.display_name

    for parse in parses:
        output = parse(message.content)
        if output == None:
            continue
        if "name" in output:
            await client.change_nickname(message.server.me, output["name"])
        if "message" in output:
            await client.send_message(message.channel, output["message"])
        if "name" in output:
            await client.change_nickname(message.server.me, previous_name)
        if output:
            return

