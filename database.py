from pymongo import MongoClient
from random import randrange

client = MongoClient()
db = client.nicknames

serverStatusResult = db.command("serverStatus")

def remove_all_names(id_num):
    db.nicknames.remove({'id': id_num})
    return

def get_nickname(id_num, original):
    nicknames_db = db.nicknames.find({'id': id_num})
    nicknames = []
    for nickname in nicknames_db:
        nicknames.append(nickname["nickname"])
    nickname = False
    if len(nicknames) < 2:
        if len(nicknames) == 0:
            return original
        return nicknames[0]
    while nickname == False or nickname == original:
        nickname = nicknames[randrange(len(nicknames))]
    return nickname 

def remove_nickname(id_num, nickname):
    if nickname.isdigit():
        nickname = int(nickname)
        nickname = list_names(id_num)[nickname-1]
    nicknames = db.nicknames.remove({"nickname": nickname})

def add_nickname(id_num, nickname):
    nickname = nickname.strip()
    if len(nickname) > 32:
        return f"Error: nickname '{nickname}' is longer than 32 characters!"
    elif len(nickname) < 1:
        return f"Error: no nickname given. Try `/addname name`"
    matches = db.nicknames.find({'id': id_num, 'nickname': nickname})
    if matches.count() > 0:
        return f"Error: nickname '{nickname}' already exists!"
    post_data = {
        "nickname": nickname,
        "id": id_num,
    }
    db.nicknames.insert_one(post_data)
    return f"Successfully added nickname '{nickname}' to <@{id_num}>'s user bank."


def list_names(id_num):
    nicknames = db.nicknames.find({'id': id_num})
    name_list = []

    for index, nickname in enumerate(nicknames):
        name_list.append(nickname['nickname'])

    return name_list

def pprint_names(id_num):
    names = list_names(id_num)
    name_list = ""
    for index in range(len((names))):
        name_list += f"{index + 1}. {names[index]}\n"

    return name_list
