from pymongo import MongoClient
from random import choice

client = MongoClient(port=27018)
db = client.nicknames

serverStatusResult = db.command("serverStatus")

def remove_all_names(id_num):
    db.nicknames.update_one({'id': id_num}, )
    return

def get_nickname(id_num, original):
    nicknames = list_names(id_num)
    nickname = False
    if len(nicknames) < 2:
        if len(nicknames) == 0:
            return original
        return nicknames[0]
    while nickname == False or nickname == original:
        nickname = choice(nicknames)
    return nickname 

def remove_nickname(id_num, nickname):
    if nickname.isdigit():
        nickname = int(nickname)
        nickname = list_names(id_num)[nickname-1]
    archive_names(id_num, [nickname])

def add_nickname(id_num, nickname):
    nickname = nickname.strip()
    if len(nickname) > 32:
        return f"Error: nickname '{nickname}' is longer than 32 characters!"
    elif len(nickname) < 1:
        return f"Error: no nickname given. Try `/addname name`"
    matches = db.nicknames.find({'id': id_num, 'nickname': nickname})
    if matches.count() > 0:
        for match in matches:
            if not match['archived']:
                return f"Error: nickname '{nickname}' already exists!"
            else:
                archive_names(id_num, [nickname], archive=False)
                return f"Successfully restored nickname: '{nickname}'!"
    post_data = {
        "nickname": nickname,
        "id": id_num,
    }
    db.nicknames.insert_one(post_data)
    return f"Successfully added nickname '{nickname}' to <@{id_num}>'s user bank."

def archive_names(id_num, nicknames, archive = True):
    if nicknames == None:
        db.nicknames.update_many({'id': id_num},{'$set': {"archived": archive}})
    for nickname in nicknames:
        db.nicknames.update_one({'id': id_num, 'nickname': nickname}, 
            {'$set': {"archived": archive}})


def list_names(id_num, query = "default"):
    nicknames = db.nicknames.find({'id': id_num})
    name_list = []
    for index, nickname in enumerate(nicknames):
        if( 
            query == "default" and not('archived' in nickname) or
            query == "archived" and 'archived' in nickname or
            query == "all"
        ):
            name_list.append(nickname['nickname'])
    return name_list


def pprint_names(id_num, query = "default"):
    names = list_names(id_num, query)
    name_list = f"Name list for <@{id_num}>:\n"
    for index in range(len((names))):
        name_list += f"{index + 1}. {names[index]}\n"

    return name_list
